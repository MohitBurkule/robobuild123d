' ===== sw_gen interpreter (SolidWorks 2025, late bound) =====================================
' Executes rebuild ops ("KIND|arg|arg|...") produced by rebuild_dump/sw_gen from a SolidWorks API dump.
' Lessons kept from the RV01 runs (sw_run1..5): AddToDB sketching, typed numeric arguments only,
' rename the sketch feature after leaving the sketch, mirror plane mark 2 + seed features mark 1,
' blend edges picked by enumerating the body's edges (never SelectByID2 point picks),
' no SKETCHREGION point picks (profiles = whole sketch, SketchContour objects, or an outline sketch).
' Every op logs OK / FAIL / SKIP / WARN; features log the body volume against the replay volume.

Dim swApp As Object
Dim mu As Object
Dim logPath As String
Dim nOK As Long, nFail As Long, nSkip As Long, nWarn As Long
Dim gExpect As Double, gExpectTag As String
Dim gPartName As String
Dim gFinalReplay As Double, gFinalMass As Double, gFinalKg As Double
' active sketch state
Dim gSk As Object
Dim gTr(12) As Double            ' active sketch ModelToSketchTransform ArrayData (9 rot, 3 trans, scale)
Dim gSkName As String
Dim A11 As Double, A12 As Double, A21 As Double, A22 As Double, B1 As Double, B2 As Double, gDet As Double
Dim gFrameMode As String          ' SAME | AXES | SWAP | ROT
Dim gSegs As Object               ' key -> sketch segment (current sketch)
Dim gAll As Object                ' sketch#key -> segment (all sketches, for revolve axes)
Dim gGeo As Object                ' sketch#key -> live geometry "L|x0|y0|x1|y1" / "A|cx|cy|r|x0|y0|x1|y1" / "C|cx|cy|r"
Dim gCont As Object               ' sketch#idx -> "k1;k2;..."
Dim gFlip As Object               ' sketch -> True when the live sketch normal opposes the dump's
Dim gFrame As Object              ' sketch -> "x0..x2|y..|n..|o.."
Dim gSupport As Object            ' sketch -> support op line
' pending selections for the next feature
Dim gEdges As Collection
Dim gBoxes As Collection
Dim gUpto As Collection
Dim gShow As Boolean
Dim gRelOK As Long, gRelFail As Long, gDimOK As Long, gDimFail As Long

Function D(ByVal s As String) As Double
    D = Val(s)
End Function

Function B(ByVal s As String) As Boolean
    B = (Trim(s) = "1" Or LCase(Trim(s)) = "true")
End Function

Sub LogLine(ByVal s As String)
    Dim fn As Integer
    fn = FreeFile
    Open logPath For Append As #fn
    Print #fn, Format(Now, "hh:nn:ss") & "  " & s
    Close #fn
End Sub

Sub LogErr(ByVal what As String)
    If Err.Number <> 0 Then
        LogLine "  ERR " & what & ": " & Err.Number & " " & Err.Description
        nWarn = nWarn + 1
    End If
    Err.Clear
End Sub

Function F6(ByVal x As Double) As String
    F6 = Format(x, "0.000000")
End Function

Function TotalVolume(ByVal m As Object, ByRef nb As Long) As Double
    On Error Resume Next
    Dim bodies As Variant, i As Long, v As Double, mp As Variant
    v = 0: nb = 0
    bodies = m.GetBodies2(0, True)
    If IsArray(bodies) Then
        nb = UBound(bodies) + 1
        For i = 0 To UBound(bodies)
            mp = bodies(i).GetMassProperties(1)
            If IsArray(mp) Then v = v + mp(3)
        Next
    End If
    Err.Clear
    TotalVolume = v
End Function

Sub LogVolume(ByVal m As Object)
    On Error Resume Next
    Dim v As Double, nb As Long, s As String
    v = TotalVolume(m, nb)
    s = "       bodies=" & nb & " volume=" & Format(v * 1E+9, "0.0") & " mm3"
    If gExpect > 0 Then
        s = s & "  replay=" & Format(gExpect * 1E+9, "0.0") & " mm3 (" & gExpectTag & ") diff=" & Format((v - gExpect) / gExpect * 100, "0.00") & "%"
    End If
    LogLine s
    If gShow Then
        m.GraphicsRedraw2
    End If
    Err.Clear
End Sub

Function Report(ByVal m As Object, ByVal feat As Object, ByVal nm As String, ByVal extra As String) As Boolean
    Dim en As Long, ed As String
    en = Err.Number: ed = Err.Description
    Err.Clear
    On Error Resume Next
    If feat Is Nothing Then
        nFail = nFail + 1
        If en <> 0 Then
            LogLine "FAIL " & nm & " " & extra & " err=" & en & " " & ed
        Else
            LogLine "FAIL " & nm & " " & extra & " (API returned Nothing)"
        End If
        Report = False
    Else
        feat.Name = nm
        If Err.Number <> 0 Then LogLine "  WARN rename to " & nm & " failed: " & Err.Description: Err.Clear
        nOK = nOK + 1
        LogLine "OK   " & nm & " " & extra
        Report = True
    End If
    LogVolume m
    gExpect = 0: gExpectTag = ""
    Err.Clear
End Function

' ---------------------------------------------------------------------------- transforms
Function LoadTr() As Boolean
    ' read the live ModelToSketchTransform once per sketch and apply it by hand (as the working
    ' RV01_rebuild_macro does). MathPoint.MultiplyTransform on the cached sketch object returned the
    ' translation only (every point -> the same sketch point) in SolidWorks: A = 0, no entity created.
    On Error Resume Next
    Dim v As Variant, i As Integer
    LoadTr = False
    v = gSk.ModelToSketchTransform.ArrayData
    If Not IsArray(v) Then v = swApp.ActiveDoc.SketchManager.ActiveSketch.ModelToSketchTransform.ArrayData
    If Not IsArray(v) Then Exit Function
    For i = 0 To 12: gTr(i) = CDbl(v(i)): Next
    If Abs(gTr(12)) < 1E-12 Then gTr(12) = 1
    LoadTr = True
    Err.Clear
End Function

Function M2S(ByVal x As Double, ByVal y As Double, ByVal z As Double) As Variant
    Dim q(2) As Double, i As Integer
    For i = 0 To 2
        q(i) = gTr(12) * (x * gTr(i) + y * gTr(3 + i) + z * gTr(6 + i)) + gTr(9 + i)
    Next
    M2S = q
End Function

Sub MapUV(ByVal u As Double, ByVal v As Double, ByRef x As Double, ByRef y As Double)
    x = A11 * u + A12 * v + B1
    y = A21 * u + A22 * v + B2
End Sub

Sub UnmapXY(ByVal x As Double, ByVal y As Double, ByRef u As Double, ByRef v As Double)
    Dim dx As Double, dy As Double
    dx = x - B1: dy = y - B2
    If Abs(gDet) < 1E-30 Then u = dx: v = dy: Exit Sub
    u = (A22 * dx - A12 * dy) / gDet
    v = (-A21 * dx + A11 * dy) / gDet
End Sub

' ---------------------------------------------------------------------------- selection helpers
Function SelData(ByVal m As Object, ByVal mark As Long) As Object
    Dim sd As Object
    Set sd = m.SelectionManager.CreateSelectData
    sd.Mark = mark
    Set SelData = sd
End Function

Function SelCount(ByVal m As Object) As Long
    On Error Resume Next
    SelCount = m.SelectionManager.GetSelectedObjectCount2(-1)
    Err.Clear
End Function

' planar model face coplanar with (n, o), nearest to c
Function FindPlanarFace(ByVal m As Object, ByVal nx As Double, ByVal ny As Double, ByVal nz As Double, _
        ByVal ox As Double, ByVal oy As Double, ByVal oz As Double, ByVal cx As Double, ByVal cy As Double, ByVal cz As Double, ByRef dist As Double) As Object
    On Error Resume Next
    Dim bodies As Variant, faces As Variant, i As Long, j As Long, srf As Object, pp As Variant
    Dim dt As Double, off As Double, cp As Variant, d As Double, best As Object, bd As Double
    bd = 1E+30
    bodies = m.GetBodies2(0, True)
    If IsArray(bodies) Then
        For i = 0 To UBound(bodies)
            faces = bodies(i).GetFaces
            If IsArray(faces) Then
                For j = 0 To UBound(faces)
                    Set srf = faces(j).GetSurface
                    If Not srf Is Nothing Then
                        If srf.IsPlane Then
                            pp = srf.PlaneParams
                            dt = pp(0) * nx + pp(1) * ny + pp(2) * nz
                            If Abs(Abs(dt) - 1) < 0.000001 Then
                                off = (pp(3) - ox) * nx + (pp(4) - oy) * ny + (pp(5) - oz) * nz
                                If Abs(off) < 0.0000005 Then
                                    cp = faces(j).GetClosestPointOn(cx, cy, cz)
                                    If IsArray(cp) Then
                                        d = Sqr((cp(0) - cx) ^ 2 + (cp(1) - cy) ^ 2 + (cp(2) - cz) ^ 2)
                                        If d < bd Then bd = d: Set best = faces(j)
                                    End If
                                End If
                            End If
                        End If
                    End If
                Next
            End If
        Next
    End If
    Err.Clear
    dist = bd
    Set FindPlanarFace = best
End Function

Function StdPlaneOf(ByVal nx As Double, ByVal ny As Double, ByVal nz As Double) As String
    StdPlaneOf = ""
    If Abs(Abs(nz) - 1) < 0.000001 Then StdPlaneOf = "Front Plane"
    If Abs(Abs(ny) - 1) < 0.000001 Then StdPlaneOf = "Top Plane"
    If Abs(Abs(nx) - 1) < 0.000001 Then StdPlaneOf = "Right Plane"
End Function

' plane through 3 points (3D sketch points); returns the plane feature
Function Plane3P(ByVal m As Object, ByVal nm As String, ByVal ox As Double, ByVal oy As Double, ByVal oz As Double, _
        ByVal xx As Double, ByVal xy As Double, ByVal xz As Double, ByVal yx As Double, ByVal yy As Double, ByVal yz As Double) As Object
    On Error Resume Next
    Dim p0 As Object, p1 As Object, p2 As Object, f As Object, sc As Double
    sc = 0.01
    m.ClearSelection2 True
    m.SketchManager.Insert3DSketch True
    m.SketchManager.AddToDB = True
    Set p0 = m.SketchManager.CreatePoint(ox, oy, oz)
    Set p1 = m.SketchManager.CreatePoint(ox + sc * xx, oy + sc * xy, oz + sc * xz)
    Set p2 = m.SketchManager.CreatePoint(ox + sc * yx, oy + sc * yy, oz + sc * yz)
    m.SketchManager.AddToDB = False
    m.SketchManager.Insert3DSketch True
    LogErr "3D sketch points for " & nm
    m.FeatureByPositionReverse(0).Name = nm & "_pts"
    Err.Clear
    m.ClearSelection2 True
    p0.Select4 False, SelData(m, 0)
    p1.Select4 True, SelData(m, 1)
    p2.Select4 True, SelData(m, 2)
    Set f = m.FeatureManager.InsertRefPlane(4, 0, 4, 0, 4, 0)
    LogErr "InsertRefPlane(3 points) " & nm
    Set Plane3P = f
End Function

' reference axis through two points (3D sketch points + InsertAxis2); returns the axis feature name
Function Axis2P(ByVal m As Object, ByVal nm As String, ByVal ox As Double, ByVal oy As Double, ByVal oz As Double, _
        ByVal ax As Double, ByVal ay As Double, ByVal az As Double) As String
    On Error Resume Next
    Dim p0 As Object, p1 As Object, sc As Double, ok As Boolean
    sc = 0.01
    Axis2P = ""
    m.ClearSelection2 True
    m.SketchManager.Insert3DSketch True
    m.SketchManager.AddToDB = True
    Set p0 = m.SketchManager.CreatePoint(ox, oy, oz)
    Set p1 = m.SketchManager.CreatePoint(ox + sc * ax, oy + sc * ay, oz + sc * az)
    m.SketchManager.AddToDB = False
    m.SketchManager.Insert3DSketch True
    m.FeatureByPositionReverse(0).Name = nm & "_pts"
    Err.Clear
    m.ClearSelection2 True
    p0.Select4 False, SelData(m, 0)
    p1.Select4 True, SelData(m, 0)
    ok = m.InsertAxis2(True)
    LogErr "InsertAxis2 " & nm
    If ok Then
        m.FeatureByPositionReverse(0).Name = nm
        Err.Clear
        Axis2P = nm
    Else
        LogLine "  WARN axis " & nm & " not created"
    End If
End Function

Sub HideRefs(ByVal m As Object)
    On Error Resume Next
    Dim ft As Object, tn As String
    Set ft = m.FirstFeature
    Do While Not ft Is Nothing
        tn = ft.GetTypeName2
        If tn = "RefPlane" Or tn = "ProfileFeature" Or tn = "3DProfileFeature" Or tn = "RefAxis" Then
            m.ClearSelection2 True
            ft.Select2 False, 0
            If tn = "RefPlane" Or tn = "RefAxis" Then m.BlankRefGeom Else m.BlankSketch
        End If
        Set ft = ft.GetNextFeature
    Loop
    m.ClearSelection2 True
    Err.Clear
End Sub

' ---------------------------------------------------------------------------- ops
Sub OpRefPlane(ByVal m As Object, ByVal a As Variant)
    On Error Resume Next
    Dim nm As String, mode As String, par As String, dist As Double, flp As Boolean, f As Object, opt As Long
    nm = a(1): mode = a(2): par = a(3): dist = D(a(4)): flp = B(a(5))
    m.ClearSelection2 True
    If mode = "OFFSET" Or mode = "COINCIDENT" Then
        If Not m.Extension.SelectByID2(par, "PLANE", 0, 0, 0, False, 0, Nothing, 0) Then
            LogLine "  WARN parent plane " & par & " not selectable"
        End If
        If mode = "OFFSET" Then
            opt = 8
            If flp Then opt = 8 + 256
            Set f = m.FeatureManager.InsertRefPlane(opt, dist, 0, 0, 0, 0)
        Else
            Set f = m.FeatureManager.InsertRefPlane(4, 0, 0, 0, 0, 0)
        End If
        LogErr "InsertRefPlane"
        Report m, f, nm, mode & " " & par & " d=" & dist & " flip=" & flp
    Else
        Set f = Plane3P(m, nm, D(a(9)), D(a(10)), D(a(11)), D(a(12)), D(a(13)), D(a(14)), D(a(15)), D(a(16)), D(a(17)))
        Report m, f, nm, "3 points (angle/other references not dumped)"
    End If
    m.ClearSelection2 True
End Sub

Sub OpSketch(ByVal m As Object, ByVal a As Variant, ByVal raw As String)
    On Error Resume Next
    Dim nm As String, kind As String, pn As String, ok As Boolean, fc As Object, dist As Double, f As Object, sp As String
    nm = a(1): kind = a(2): pn = a(3)
    gSupport(nm) = raw
    m.ClearSelection2 True
    ok = False
    If kind = "PLANE" Then
        ok = m.Extension.SelectByID2(pn, "PLANE", 0, 0, 0, False, 0, Nothing, 0)
        If Not ok Then LogLine "  WARN plane " & pn & " not selectable for " & nm
    Else
        Set fc = FindPlanarFace(m, D(a(4)), D(a(5)), D(a(6)), D(a(7)), D(a(8)), D(a(9)), D(a(10)), D(a(11)), D(a(12)), dist)
        If Not fc Is Nothing Then
            ok = fc.Select4(False, SelData(m, 0))
            LogLine "  sketch " & nm & " on model face (" & Format(dist * 1000, "0.000") & " mm from profile centre)"
        Else
            LogLine "  WARN no coplanar model face for " & nm & ": using a reference plane"
        End If
    End If
    If Not ok Then
        sp = StdPlaneOf(D(a(4)), D(a(5)), D(a(6)))
        m.ClearSelection2 True
        If sp <> "" Then
            dist = D(a(7)) * Abs(D(a(4))) + D(a(8)) * Abs(D(a(5))) + D(a(9)) * Abs(D(a(6)))
            If Abs(dist) < 0.0000001 Then
                ok = m.Extension.SelectByID2(sp, "PLANE", 0, 0, 0, False, 0, Nothing, 0)
            Else
                m.Extension.SelectByID2 sp, "PLANE", 0, 0, 0, False, 0, Nothing, 0
                If dist < 0 Then
                    Set f = m.FeatureManager.InsertRefPlane(8 + 256, Abs(dist), 0, 0, 0, 0)
                Else
                    Set f = m.FeatureManager.InsertRefPlane(8, Abs(dist), 0, 0, 0, 0)
                End If
                If Not f Is Nothing Then f.Name = nm & "_plane": m.ClearSelection2 True: ok = f.Select2(False, 0)
            End If
        Else
            Dim fr As Variant
            fr = Split(gFrame(nm), "|")
            Set f = Nothing
            LogLine "  WARN " & nm & ": oblique support, 3-point plane"
        End If
        Err.Clear
    End If
    m.SketchManager.InsertSketch True
    LogErr "InsertSketch " & nm
    Set gSk = m.SketchManager.ActiveSketch
    If gSk Is Nothing Then
        LogLine "FAIL sketch " & nm & ": no active sketch"
        nFail = nFail + 1
        Exit Sub
    End If
    m.SketchManager.AddToDB = True
    m.SketchManager.DisplayWhenAdded = False
    gSkName = nm
    Set gSegs = CreateObject("Scripting.Dictionary")
    A11 = 1: A12 = 0: A21 = 0: A22 = 1: B1 = 0: B2 = 0: gDet = 1: gFrameMode = "SAME"
End Sub

Sub OpFrame(ByVal m As Object, ByVal a As Variant)
    On Error Resume Next
    Dim xx As Double, xy As Double, xz As Double, yx As Double, yy As Double, yz As Double
    Dim nx As Double, ny As Double, nz As Double, ox As Double, oy As Double, oz As Double
    Dim s0 As Variant, su As Variant, sv As Variant, offp As Double, msg As String
    Dim v(2) As Double, w As Object, ln As Variant, dt As Double
    xx = D(a(2)): xy = D(a(3)): xz = D(a(4)): yx = D(a(5)): yy = D(a(6)): yz = D(a(7))
    nx = D(a(8)): ny = D(a(9)): nz = D(a(10)): ox = D(a(11)): oy = D(a(12)): oz = D(a(13))
    gFrame(a(1)) = Join(Array(a(2), a(3), a(4), a(5), a(6), a(7), a(8), a(9), a(10), a(11), a(12), a(13)), "|")
    If gSk Is Nothing Then Exit Sub
    If Not LoadTr() Then LogLine "  WARN no sketch transform": Exit Sub
    s0 = M2S(ox, oy, oz)
    su = M2S(ox + xx, oy + xy, oz + xz)
    sv = M2S(ox + yx, oy + yy, oz + yz)
    If Not IsArray(s0) Then LogLine "  WARN no sketch transform": Exit Sub
    A11 = su(0) - s0(0): A21 = su(1) - s0(1)
    A12 = sv(0) - s0(0): A22 = sv(1) - s0(1)
    B1 = s0(0): B2 = s0(1)
    gDet = A11 * A22 - A12 * A21
    offp = Abs(s0(2)) + Abs(su(2) - s0(2)) + Abs(sv(2) - s0(2))
    If Abs(A11 - 1) + Abs(A22 - 1) + Abs(A12) + Abs(A21) + Abs(B1) + Abs(B2) < 0.000001 Then
        gFrameMode = "SAME"
    ElseIf Abs(A12) + Abs(A21) < 0.000001 Then
        gFrameMode = "AXES"
    ElseIf Abs(A11) + Abs(A22) < 0.000001 Then
        gFrameMode = "SWAP"
    Else
        gFrameMode = "ROT"
    End If
    ' live sketch normal in model space vs dump normal
    ' sketch z axis in model space: row-vector convention q = sc * p * R + t -> R column 2
    ln = Array(gTr(2), gTr(5), gTr(8))
    dt = ln(0) * nx + ln(1) * ny + ln(2) * nz
    gFlip(a(1)) = (dt < 0)
    msg = "  frame " & a(1) & ": " & gFrameMode & " A=[" & Format(A11, "0.000") & "," & Format(A12, "0.000") & ";" & Format(A21, "0.000") & "," & Format(A22, "0.000") & _
          "] b=(" & Format(B1 * 1000, "0.000") & "," & Format(B2 * 1000, "0.000") & ") mm  normal " & IIf(dt < 0, "FLIPPED", "same") & _
          "  off-plane=" & Format(offp * 1000, "0.0000") & " mm"
    If offp > 0.000001 Then
        LogLine "  WARN FRAME MISMATCH" & msg
        nWarn = nWarn + 1
    Else
        LogLine msg
    End If
    Err.Clear
End Sub

Sub KeepSeg(ByVal key As String, ByVal sg As Object, ByVal geo As String, ByVal constr As Boolean)
    On Error Resume Next
    If sg Is Nothing Then
        LogLine "  WARN entity " & key & " not created"
        nWarn = nWarn + 1
        Exit Sub
    End If
    If constr Then sg.ConstructionGeometry = True
    Set gSegs(key) = sg
    Set gAll(gSkName & "#" & key) = sg
    gGeo(gSkName & "#" & key) = geo
    Err.Clear
End Sub

Function LastSeg() As Object
    On Error Resume Next
    Dim v As Variant
    Set LastSeg = Nothing
    v = gSk.GetSketchSegments
    If IsArray(v) Then Set LastSeg = v(UBound(v))
    Err.Clear
End Function

Sub OpLine(ByVal m As Object, ByVal a As Variant)
    On Error Resume Next
    Dim x0 As Double, y0 As Double, x1 As Double, y1 As Double, sg As Object
    MapUV D(a(3)), D(a(4)), x0, y0
    MapUV D(a(5)), D(a(6)), x1, y1
    Set sg = m.SketchManager.CreateLine(x0, y0, 0#, x1, y1, 0#)
    If sg Is Nothing Then
        Err.Clear
        m.SketchManager.CreateLine x0, y0, 0#, x1, y1, 0#
        Set sg = LastSeg()
    End If
    LogErr "CreateLine " & a(1)
    KeepSeg a(1), sg, "L|" & x0 & "|" & y0 & "|" & x1 & "|" & y1, B(a(2))
End Sub

Sub OpArc(ByVal m As Object, ByVal a As Variant)
    On Error Resume Next
    Dim xc As Double, yc As Double, x0 As Double, y0 As Double, x1 As Double, y1 As Double, dr As Integer, sg As Object, r As Double
    MapUV D(a(3)), D(a(4)), xc, yc
    MapUV D(a(5)), D(a(6)), x0, y0
    MapUV D(a(7)), D(a(8)), x1, y1
    dr = CInt(D(a(9)))
    If gDet < 0 Then dr = -dr
    Set sg = m.SketchManager.CreateArc(xc, yc, 0#, x0, y0, 0#, x1, y1, 0#, dr)
    If sg Is Nothing Then
        Err.Clear
        m.SketchManager.CreateArc xc, yc, 0#, x0, y0, 0#, x1, y1, 0#, dr
        Set sg = LastSeg()
    End If
    LogErr "CreateArc " & a(1)
    r = Sqr((x0 - xc) ^ 2 + (y0 - yc) ^ 2)
    KeepSeg a(1), sg, "A|" & xc & "|" & yc & "|" & r & "|" & x0 & "|" & y0 & "|" & x1 & "|" & y1, B(a(2))
End Sub

Sub OpCircle(ByVal m As Object, ByVal a As Variant)
    On Error Resume Next
    Dim xc As Double, yc As Double, r As Double, sg As Object
    MapUV D(a(3)), D(a(4)), xc, yc
    r = D(a(5)) * Sqr(Abs(gDet))
    Set sg = m.SketchManager.CreateCircleByRadius(xc, yc, 0#, r)
    If sg Is Nothing Then
        Err.Clear
        m.SketchManager.CreateCircleByRadius xc, yc, 0#, r
        Set sg = LastSeg()
    End If
    LogErr "CreateCircleByRadius " & a(1)
    KeepSeg a(1), sg, "C|" & xc & "|" & yc & "|" & r, B(a(2))
End Sub

Sub OpSpline(ByVal m As Object, ByVal a As Variant)
    ' SPLINE|key|constr|n|u0|v0|...: spline through n points (sketch space)
    On Error Resume Next
    Dim n As Long, i As Long, x As Double, y As Double, pd() As Double, sg As Object, x0 As Double, y0 As Double
    n = CLng(D(a(3)))
    If n < 2 Then Exit Sub
    ReDim pd(3 * n - 1)
    For i = 0 To n - 1
        MapUV D(a(4 + 2 * i)), D(a(5 + 2 * i)), x, y
        pd(3 * i) = x: pd(3 * i + 1) = y: pd(3 * i + 2) = 0#
        If i = 0 Then x0 = x: y0 = y
    Next
    Set sg = m.SketchManager.CreateSpline2((pd), False)
    If sg Is Nothing Then
        Err.Clear
        Set sg = m.SketchManager.CreateSpline((pd))
    End If
    If sg Is Nothing Then Set sg = LastSeg()
    LogErr "CreateSpline2 " & a(1)
    KeepSeg a(1), sg, "S|" & x0 & "|" & y0 & "|" & x & "|" & y, B(a(2))
End Sub

Sub OpPoint(ByVal m As Object, ByVal a As Variant)
    On Error Resume Next
    Dim x As Double, y As Double, p As Object
    MapUV D(a(2)), D(a(3)), x, y
    Set p = m.SketchManager.CreatePoint(x, y, 0#)
    LogErr "CreatePoint " & a(1)
    If p Is Nothing Then LogLine "  WARN point " & a(1) & " not created"
End Sub

' sketch points of the active sketch at live (x, y)
Function PointsAt(ByVal x As Double, ByVal y As Double) As Collection
    On Error Resume Next
    Dim c As New Collection, v As Variant, i As Long
    v = gSk.GetSketchPoints2
    If IsArray(v) Then
        For i = 0 To UBound(v)
            If Abs(v(i).X - x) < 0.0000001 And Abs(v(i).Y - y) < 0.0000001 Then c.Add v(i)
        Next
    End If
    Err.Clear
    Set PointsAt = c
End Function

Sub OpMerge(ByVal m As Object, ByVal a As Variant)
    On Error Resume Next
    Dim x As Double, y As Double, c As Collection, it As Integer, n0 As Long
    MapUV D(a(1)), D(a(2)), x, y
    For it = 1 To 8
        Set c = PointsAt(x, y)
        If c.Count < 2 Then Exit For
        If it = 1 Then n0 = c.Count
        m.ClearSelection2 True
        c(1).Select4 False, SelData(m, 0)
        c(2).Select4 True, SelData(m, 0)
        m.SketchAddConstraints "sgMERGEPOINTS"
        If Err.Number <> 0 Then LogErr "merge": Exit For
        If PointsAt(x, y).Count >= c.Count Then Exit For
    Next
    m.ClearSelection2 True
    Err.Clear
End Sub

' select one op reference: S:key | P:u:v | O
Function SelRef(ByVal m As Object, ByVal r As String, ByVal app As Boolean, ByVal mark As Long) As Boolean
    On Error Resume Next
    Dim p As Variant, x As Double, y As Double, c As Collection
    SelRef = False
    p = Split(r, ":")
    If p(0) = "S" Then
        If gSegs.Exists(p(1)) Then SelRef = gSegs(p(1)).Select4(app, SelData(m, mark))
    ElseIf p(0) = "P" Then
        MapUV D(p(1)), D(p(2)), x, y
        Set c = PointsAt(x, y)
        If c.Count > 0 Then SelRef = c(1).Select4(app, SelData(m, mark))
    ElseIf p(0) = "O" Then
        SelRef = m.Extension.SelectByID2("Point1@Origin", "EXTSKETCHPOINT", 0, 0, 0, app, mark, Nothing, 0)
    End If
    Err.Clear
End Function

Function SelRefs(ByVal m As Object, ByVal refs As String) As Boolean
    Dim r As Variant, ok As Boolean, first As Boolean
    ok = True: first = True
    m.ClearSelection2 True
    For Each r In Split(refs, ";")
        ok = SelRef(m, CStr(r), Not first, 0) And ok
        first = False
    Next
    SelRefs = ok
End Function

' H/V relations and dimensions follow the dump's sketch axes; remap them when the live frame differs
Function HV(ByVal s As String) As String
    HV = s
    If gFrameMode = "SAME" Or gFrameMode = "AXES" Then Exit Function
    If gFrameMode = "SWAP" Then
        Select Case s
            Case "sgHORIZONTAL2D": HV = "sgVERTICAL2D"
            Case "sgVERTICAL2D": HV = "sgHORIZONTAL2D"
            Case "sgHORIZONTALPOINTS2D": HV = "sgVERTICALPOINTS2D"
            Case "sgVERTICALPOINTS2D": HV = "sgHORIZONTALPOINTS2D"
            Case "H": HV = "V"
            Case "V": HV = "H"
        End Select
        Exit Function
    End If
    Select Case s
        Case "sgHORIZONTAL2D", "sgVERTICAL2D", "sgHORIZONTALPOINTS2D", "sgVERTICALPOINTS2D", "H", "V": HV = ""
    End Select
End Function

Sub OpRel(ByVal m As Object, ByVal a As Variant)
    On Error Resume Next
    Dim sg As String
    sg = HV(a(1))
    If sg = "" Then LogLine "  skip " & a(1) & " (sketch frame rotated)": Exit Sub
    If Not SelRefs(m, a(2)) Then
        LogLine "  WARN rel " & sg & " " & a(2) & ": selection incomplete"
        gRelFail = gRelFail + 1
        m.ClearSelection2 True
        Exit Sub
    End If
    m.SketchAddConstraints sg
    If Err.Number <> 0 Then
        LogErr "SketchAddConstraints " & sg & " " & a(2)
        gRelFail = gRelFail + 1
    Else
        gRelOK = gRelOK + 1
    End If
    m.ClearSelection2 True
End Sub

Sub OpDim(ByVal m As Object, ByVal a As Variant)
    On Error Resume Next
    Dim kind As String, val0 As Double, x As Double, y As Double, dd As Object, dm As Object, cur As Double, ok As Boolean
    kind = HV(a(1))
    If kind = "" Then kind = "AUTO"
    val0 = D(a(3))
    MapUV D(a(4)), D(a(5)), x, y
    If Not SelRefs(m, a(2)) Then
        LogLine "  WARN dim " & a(6) & ": selection incomplete"
        gDimFail = gDimFail + 1
        m.ClearSelection2 True
        Exit Sub
    End If
    Select Case kind
        Case "H": Set dd = m.AddHorizontalDimension2(x, y, 0)
        Case "V": Set dd = m.AddVerticalDimension2(x, y, 0)
        Case "RAD": Set dd = m.AddRadialDimension2(x, y, 0)
        Case "DIA": Set dd = m.AddDiameterDimension2(x, y, 0)
        Case Else: Set dd = m.AddDimension2(x, y, 0)
    End Select
    LogErr "AddDimension " & kind & " " & a(6)
    If dd Is Nothing Then
        gDimFail = gDimFail + 1
        m.ClearSelection2 True
        Exit Sub
    End If
    Set dm = dd.GetDimension2(0)
    cur = dm.SystemValue
    ok = Abs(cur - val0) < 0.000001
    If Not ok And kind = "ANG" Then ok = Abs((3.14159265358979 - cur) - val0) < 0.000001
    If ok Then
        dm.SystemValue = val0
        dm.Name = a(6)
        Err.Clear
        gDimOK = gDimOK + 1
    Else
        LogLine "  WARN dim " & a(6) & " (" & kind & ") measured " & cur & " expected " & val0 & ": removed"
        m.ClearSelection2 True
        dd.GetAnnotation.Select3 False, Nothing
        m.EditDelete
        gDimFail = gDimFail + 1
    End If
    m.ClearSelection2 True
    Err.Clear
End Sub

Sub OpContour(ByVal a As Variant)
    gCont(gSkName & "#" & a(1)) = a(2)
End Sub

Function StatusName(ByVal s As Long) As String
    Select Case s
        Case 1: StatusName = "unknown"
        Case 2: StatusName = "UNDER-defined"
        Case 3: StatusName = "fully defined"
        Case 4: StatusName = "OVER-defined"
        Case 5: StatusName = "no solution"
        Case 6: StatusName = "invalid solution"
        Case 7: StatusName = "autosolve off"
        Case Else: StatusName = "status " & s
    End Select
End Function

Sub OpEndSketch(ByVal m As Object, ByVal a As Variant)
    On Error Resume Next
    Dim n As Long, segs As Variant, st As Long, nm As String
    nm = a(1)
    If gSk Is Nothing Then Exit Sub
    segs = gSk.GetSketchSegments
    If IsArray(segs) Then n = UBound(segs) + 1
    st = gSk.GetConstrainedStatus
    Err.Clear
    m.SketchManager.AddToDB = False
    m.SketchManager.DisplayWhenAdded = True
    m.SketchManager.InsertSketch True
    LogErr "InsertSketch(exit) " & nm
    m.FeatureByPositionReverse(0).Name = nm
    If Err.Number <> 0 Then LogLine "  WARN sketch rename " & nm & ": " & Err.Description: Err.Clear
    LogLine "OK   sketch " & nm & " segments=" & n & "/" & a(2) & " rels " & gRelOK & " ok " & gRelFail & " failed / " & a(3) & _
            ", dims " & gDimOK & " ok " & gDimFail & " failed / " & a(4) & " -> " & StatusName(st)
    nOK = nOK + 1
    gRelOK = 0: gRelFail = 0: gDimOK = 0: gDimFail = 0
    Set gSk = Nothing
    m.ClearSelection2 True
End Sub

' ---------------------------------------------------------------------------- profiles
Function GeoMatch(ByVal sg As Object, ByVal geo As String) As Boolean
    On Error Resume Next
    Dim g As Variant, t As Long, p0 As Object, p1 As Object, c As Object, tol As Double, sp As Variant
    tol = 0.000001
    GeoMatch = False
    g = Split(geo, "|")
    t = sg.GetType
    Set p0 = sg.GetStartPoint2: Set p1 = sg.GetEndPoint2
    If g(0) = "L" And t = 0 Then
        If (Abs(p0.X - D(g(1))) < tol And Abs(p0.Y - D(g(2))) < tol And Abs(p1.X - D(g(3))) < tol And Abs(p1.Y - D(g(4))) < tol) Or _
           (Abs(p1.X - D(g(1))) < tol And Abs(p1.Y - D(g(2))) < tol And Abs(p0.X - D(g(3))) < tol And Abs(p0.Y - D(g(4))) < tol) Then GeoMatch = True
    ElseIf g(0) = "S" And t = 3 Then
        sp = sg.GetPoints2
        If IsArray(sp) Then Set p0 = sp(0): Set p1 = sp(UBound(sp))
        If (Abs(p0.X - D(g(1))) < tol And Abs(p0.Y - D(g(2))) < tol And Abs(p1.X - D(g(3))) < tol And Abs(p1.Y - D(g(4))) < tol) Or _
           (Abs(p1.X - D(g(1))) < tol And Abs(p1.Y - D(g(2))) < tol And Abs(p0.X - D(g(3))) < tol And Abs(p0.Y - D(g(4))) < tol) Then GeoMatch = True
    ElseIf (g(0) = "A" Or g(0) = "C") And t = 1 Then
        Set c = sg.GetCenterPoint2
        If Abs(c.X - D(g(1))) < tol And Abs(c.Y - D(g(2))) < tol And Abs(sg.GetRadius - D(g(3))) < tol Then
            If g(0) = "C" Then
                GeoMatch = True
            ElseIf (Abs(p0.X - D(g(4))) < tol And Abs(p0.Y - D(g(5))) < tol) Or (Abs(p1.X - D(g(4))) < tol And Abs(p1.Y - D(g(5))) < tol) Then
                GeoMatch = True
            End If
        End If
    End If
    Err.Clear
End Function

' select the sketch's contours whose segments match contour idx (live SketchContour objects)
Function SelContours(ByVal m As Object, ByVal skn As String, ByVal sel As String, ByVal mark As Long) As Boolean
    On Error Resume Next
    Dim ft As Object, sk As Object, cs As Variant, i As Long, j As Long, k As Long, keys As Variant, idx As Variant
    Dim segs As Variant, ok As Boolean, nHit As Long, nWant As Long, hit As Boolean, first As Boolean
    SelContours = False
    Set ft = m.FeatureByName(skn)
    If ft Is Nothing Then Exit Function
    Set sk = ft.GetSpecificFeature2
    cs = sk.GetSketchContours
    If Not IsArray(cs) Then LogLine "  WARN " & skn & ": GetSketchContours empty": Exit Function
    m.ClearSelection2 True
    first = True
    For Each idx In Split(sel, ";")
        nWant = nWant + 1
        keys = Split(gCont(skn & "#" & idx), ";")
        For i = 0 To UBound(cs)
            segs = cs(i).GetSketchSegments
            If IsArray(segs) Then
                If UBound(segs) = UBound(keys) Then
                    ok = True
                    For j = 0 To UBound(segs)
                        hit = False
                        For k = 0 To UBound(keys)
                            If GeoMatch(segs(j), gGeo(skn & "#" & keys(k))) Then hit = True: Exit For
                        Next
                        If Not hit Then ok = False: Exit For
                    Next
                    If ok Then
                        If cs(i).Select2(Not first, mark) Then nHit = nHit + 1: first = False
                        Exit For
                    End If
                End If
            End If
        Next
    Next
    LogErr "SketchContour select"
    LogLine "  contours " & skn & " [" & sel & "]: " & nHit & "/" & nWant & " selected (mark " & mark & ")"
    SelContours = (nHit = nWant And nHit > 0)
End Function

Function SelSketch(ByVal m As Object, ByVal skn As String) As Boolean
    m.ClearSelection2 True
    SelSketch = m.Extension.SelectByID2(skn, "SKETCH", 0, 0, 0, False, 0, Nothing, 0)
End Function

' up-to references: planar face by geometry (mark 1 = direction 1, mark 2 = direction 2)
Function SelUpTo(ByVal m As Object, ByVal skn As String, ByRef depth1 As Double, ByRef depth2 As Double) As Long
    On Error Resume Next
    Dim it As Variant, a As Variant, fc As Object, dist As Double, n As Long, mk As Long, fr As Variant, cs As Variant, c As Variant
    Dim ox As Double, oy As Double, oz As Double, nx As Double, ny As Double, nz As Double, found As Boolean
    SelUpTo = 0
    For Each it In gUpto
        a = Split(it, "|")
        mk = CLng(D(a(1)))
        found = False
        If a(2) = "PLANE" Then
            Set fc = FindPlanarFace(m, D(a(3)), D(a(4)), D(a(5)), D(a(6)), D(a(7)), D(a(8)), D(a(6)), D(a(7)), D(a(8)), dist)
            If Not fc Is Nothing Then found = fc.Select4(True, SelData(m, mk))
            If UBound(a) >= 9 Then
                If mk = 1 Then depth1 = D(a(9)) Else depth2 = D(a(9))
            End If
        ElseIf a(2) = "CAPS" And gFrame.Exists(skn) Then
            fr = Split(gFrame(skn), "|")
            nx = D(fr(6)): ny = D(fr(7)): nz = D(fr(8)): ox = D(fr(9)): oy = D(fr(10)): oz = D(fr(11))
            For Each c In Split(a(3), ";")
                If c <> "none" And Not found Then
                    Set fc = FindPlanarFace(m, nx, ny, nz, ox + nx * D(c), oy + ny * D(c), oz + nz * D(c), ox, oy, oz, dist)
                    If Not fc Is Nothing Then found = fc.Select4(True, SelData(m, mk))
                End If
            Next
        End If
        If found Then
            n = n + 1
        Else
            LogLine "  WARN up-to face (dir " & mk & ") not found"
        End If
    Next
    Err.Clear
    SelUpTo = n
End Function

Function DelFeature(ByVal m As Object, ByVal f As Object) As Boolean
    On Error Resume Next
    m.ClearSelection2 True
    f.Select2 False, 0
    DelFeature = m.Extension.DeleteSelection2(0)
    Err.Clear
End Function

Sub OpExtrude(ByVal m As Object, ByVal a As Variant)
    On Error Resume Next
    Dim nm As String, isCut As Boolean, skn As String, sd As Boolean, flp As Boolean, rev As Boolean
    Dim t1 As Long, t2 As Long, d1 As Double, d2 As Double, dr1 As Boolean, dr2 As Boolean, g1 As Double, g2 As Double
    Dim mrg As Boolean, thin As Boolean, thk As Double, sel As String, f As Object, attempt As Integer, how As String
    Dim nUp As Long, need As Long, dep1 As Double, dep2 As Double, ok As Boolean
    nm = a(1): isCut = B(a(2)): skn = a(3): sd = B(a(4)): flp = B(a(5)): rev = B(a(6))
    t1 = CLng(D(a(7))): t2 = CLng(D(a(8))): d1 = D(a(9)): d2 = D(a(10))
    dr1 = B(a(11)): dr2 = B(a(12)): g1 = D(a(13)): g2 = D(a(14))
    mrg = B(a(15)): thin = B(a(16)): thk = D(a(17)): sel = a(18)
    If gFlip.Exists(skn) Then
        If gFlip(skn) Then rev = Not rev: LogLine "  " & skn & " normal flipped vs dump -> reverse=" & rev
    End If
    need = 0
    If t1 = 3 Or t1 = 4 Or t1 = 5 Or t1 = 7 Then need = need + 1
    If Not sd And (t2 = 3 Or t2 = 4 Or t2 = 5 Or t2 = 7) Then need = need + 1
    For attempt = 0 To 3
        ' profile
        If sel = "ALL" Or attempt >= 2 Then
            ok = SelSketch(m, skn): how = "sketch"
        Else
            ok = SelContours(m, skn, sel, 0): how = "contours"
            If Not ok And attempt = 0 Then ok = SelContours(m, skn, sel, 4): how = "contours(mark 4)"
            If Not ok Then ok = SelSketch(m, skn): how = "sketch(contour fallback)"
        End If
        If Not ok Then LogLine "  WARN profile selection failed for " & nm
        ' up-to references
        If need > 0 Then
            dep1 = 0: dep2 = 0
            nUp = SelUpTo(m, skn, dep1, dep2)
            If nUp < need Then
                If dep1 > 0 And (t1 = 3 Or t1 = 4 Or t1 = 7) Then LogLine "  up-to face missing: dir1 -> blind " & dep1: t1 = 0: d1 = dep1
                If dep2 > 0 And (t2 = 3 Or t2 = 4 Or t2 = 7) Then LogLine "  up-to face missing: dir2 -> blind " & dep2: t2 = 0: d2 = dep2
            End If
        End If
        If thin Then
            Set f = m.FeatureManager.FeatureExtrusionThin2(sd, flp, rev, t1, t2, d1, d2, dr1, dr2, False, False, g1, g2, False, False, False, False, mrg, _
                     thk, thk, 0, 0, False, False, 0, True, True, 0, 0, False)
            LogErr "FeatureExtrusionThin2"
        ElseIf isCut Then
            Set f = m.FeatureManager.FeatureCut4(sd, flp, rev, t1, t2, d1, d2, dr1, dr2, False, False, g1, g2, False, False, False, False, False, True, True, True, True, False, 0, 0, False, False)
            LogErr "FeatureCut4"
        Else
            Set f = m.FeatureManager.FeatureExtrusion3(sd, flp, rev, t1, t2, d1, d2, dr1, dr2, False, False, g1, g2, False, False, False, False, mrg, True, True, 0, 0, False)
            LogErr "FeatureExtrusion3"
        End If
        If Not f Is Nothing Then Exit For
        If attempt = 0 Then rev = Not rev: LogLine "  retry " & nm & " reversed"
        If attempt = 1 Then rev = Not rev: LogLine "  retry " & nm & " whole sketch"
        If attempt = 2 Then rev = Not rev: LogLine "  retry " & nm & " whole sketch reversed"
    Next
    Report m, f, nm, IIf(isCut, "cut", "boss") & " end1=" & t1 & " d1=" & d1 & IIf(sd, "", " end2=" & t2 & " d2=" & d2) & " rev=" & rev & " profile=" & how
    m.ClearSelection2 True
End Sub

Sub OpRevolve(ByVal m As Object, ByVal a As Variant)
    On Error Resume Next
    Dim nm As String, isCut As Boolean, skn As String, ak As String, oneSide As Boolean, a1 As Double, a2 As Double
    Dim rev As Boolean, mrg As Boolean, f As Object, mk As Variant, ax As Object
    nm = a(1): isCut = B(a(2)): skn = a(3): ak = a(4): oneSide = B(a(5)): a1 = D(a(6)): a2 = D(a(7)): rev = B(a(8)): mrg = B(a(9))
    For Each mk In Array(4, 16, 0, -1)
        SelSketch m, skn
        If mk >= 0 Then
            If gAll.Exists(skn & "#" & ak) Then
                Set ax = gAll(skn & "#" & ak)
                ax.Select4 True, SelData(m, CLng(mk))
            End If
        End If
        Err.Clear
        Set f = m.FeatureManager.FeatureRevolve2(oneSide, True, False, isCut, rev, False, 0, 0, a1, a2, False, False, 0, 0, 0, 0, 0, mrg, True, True)
        LogErr "FeatureRevolve2 axis mark " & mk
        If Not f Is Nothing Then Exit For
    Next
    Report m, f, nm, IIf(isCut, "revolve cut", "revolve") & " angle=" & Format(a1 * 57.2957795130823, "0.0") & " axis mark " & mk
    m.ClearSelection2 True
End Sub

' ---------------------------------------------------------------------------- blends
Function EdgePts(ByVal e As Object, ByRef p As Variant) As Boolean
    ' p(0..8): start, end, mid. Lines: chord mid point (Evaluate2 at the mean curve parameter is not the
    ' edge mid point for most lines); other curves: the curve at the mean edge parameter.
    On Error Resume Next
    Dim cp As Variant, c As Object, ev As Variant, q(8) As Double, i As Integer, isLn As Boolean
    EdgePts = False
    cp = e.GetCurveParams2
    If Not IsArray(cp) Then Exit Function
    For i = 0 To 5: q(i) = cp(i): Next
    Set c = e.GetCurve
    isLn = False
    isLn = c.IsLine
    ev = Empty
    If Not isLn Then ev = c.Evaluate2((cp(6) + cp(7)) / 2, 0)
    If IsArray(ev) Then
        q(6) = ev(0): q(7) = ev(1): q(8) = ev(2)
    Else
        q(6) = (q(0) + q(3)) / 2: q(7) = (q(1) + q(4)) / 2: q(8) = (q(2) + q(5)) / 2
    End If
    p = q
    EdgePts = True
    Err.Clear
End Function

Function Dist3(ByVal x As Double, ByVal y As Double, ByVal z As Double, ByVal u As Double, ByVal v As Double, ByVal w As Double) As Double
    Dist3 = Sqr((x - u) ^ 2 + (y - v) ^ 2 + (z - w) ^ 2)
End Function

Function CurveDist(ByVal e As Object, ByVal x As Double, ByVal y As Double, ByVal z As Double, ByVal dflt As Double) As Double
    ' distance from a point to the edge's curve, by hand from LineParams / CircleParams (no
    ' GetClosestPointOn: it gave nothing in SolidWorks and every match failed); dflt for other curves
    On Error Resume Next
    Dim c As Object, q As Variant, dx As Double, dy As Double, dz As Double, t As Double, L As Double
    Dim ax As Double, ay As Double, az As Double, h As Double, rr As Double
    CurveDist = dflt
    Set c = e.GetCurve
    If c Is Nothing Then Exit Function
    If c.IsLine Then
        q = c.LineParams
        If Not IsArray(q) Then Exit Function
        ax = q(3): ay = q(4): az = q(5): L = Sqr(ax * ax + ay * ay + az * az)
        If L = 0 Then Exit Function
        ax = ax / L: ay = ay / L: az = az / L
        dx = x - q(0): dy = y - q(1): dz = z - q(2)
        t = dx * ax + dy * ay + dz * az
        CurveDist = Sqr(Abs(dx * dx + dy * dy + dz * dz - t * t))
    ElseIf c.IsCircle Then
        q = c.CircleParams
        If Not IsArray(q) Then Exit Function
        ax = q(3): ay = q(4): az = q(5): L = Sqr(ax * ax + ay * ay + az * az)
        If L = 0 Then Exit Function
        ax = ax / L: ay = ay / L: az = az / L
        dx = x - q(0): dy = y - q(1): dz = z - q(2)
        h = dx * ax + dy * ay + dz * az
        rr = Sqr(Abs(dx * dx + dy * dy + dz * dz - h * h))
        CurveDist = Sqr(h * h + (rr - q(6)) ^ 2)
    End If
    Err.Clear
End Function

Function SelectBlendEdges(ByVal m As Object, ByVal size As Double) As Long
    ' EDGE|kind|s|e|m[|tol]: exact edges (tol absent: 0.05 mm total) or derived hints (tol = blend size based).
    ' Closed wanted edges (start = end) are matched by point-to-curve distance (seam points differ).
    On Error Resume Next
    Dim bodies As Variant, edges As Variant, i As Long, j As Long, p As Variant, it As Variant, a As Variant
    Dim best As Object, bd As Double, sc As Double, s1 As Double, s2 As Double, n As Long, used As Object, key As String, bk As String
    Dim inb As Boolean, bx As Variant, k As Integer, infl As Double, thr As Double, wcl As Boolean, ecl As Boolean
    Set used = CreateObject("Scripting.Dictionary")
    m.ClearSelection2 True
    bodies = m.GetBodies2(0, True)
    If Not IsArray(bodies) Then Exit Function
    If gEdges.Count > 0 Then
        For Each it In gEdges
            a = Split(it, "|")
            thr = 0.00005
            If UBound(a) >= 11 Then thr = 3 * D(a(11))
            wcl = Dist3(D(a(2)), D(a(3)), D(a(4)), D(a(5)), D(a(6)), D(a(7))) < 0.000000001
            Set best = Nothing: bd = 1E+30
            For i = 0 To UBound(bodies)
                edges = bodies(i).GetEdges
                If IsArray(edges) Then
                    For j = 0 To UBound(edges)
                        If EdgePts(edges(j), p) Then
                            ecl = Dist3(p(0), p(1), p(2), p(3), p(4), p(5)) < 0.000000001
                            sc = 1E+30
                            If wcl Then
                                If ecl Then
                                    If Dist3(p(6), p(7), p(8), D(a(8)), D(a(9)), D(a(10))) < 4 * thr + Dist3(p(0), p(1), p(2), p(6), p(7), p(8)) Then
                                        sc = 2 * CurveDist(edges(j), D(a(2)), D(a(3)), D(a(4)), 1E+30) + CurveDist(edges(j), D(a(8)), D(a(9)), D(a(10)), 1E+30)
                                    End If
                                End If
                            ElseIf Not ecl And UBound(a) >= 11 Then
                                ' derived hint: its points only have to lie on the live edge (edge may be longer)
                                If Dist3(p(6), p(7), p(8), D(a(8)), D(a(9)), D(a(10))) < Dist3(p(0), p(1), p(2), p(3), p(4), p(5)) / 2 + 4 * thr Then
                                    sc = CurveDist(edges(j), D(a(2)), D(a(3)), D(a(4)), 1E+30) + CurveDist(edges(j), D(a(5)), D(a(6)), D(a(7)), 1E+30) + CurveDist(edges(j), D(a(8)), D(a(9)), D(a(10)), 1E+30)
                                End If
                            ElseIf Not ecl Then
                                s1 = Dist3(p(0), p(1), p(2), D(a(2)), D(a(3)), D(a(4))) + Dist3(p(3), p(4), p(5), D(a(5)), D(a(6)), D(a(7)))
                                s2 = Dist3(p(0), p(1), p(2), D(a(5)), D(a(6)), D(a(7))) + Dist3(p(3), p(4), p(5), D(a(2)), D(a(3)), D(a(4)))
                                If s2 < s1 Then s1 = s2
                                sc = s1 + Dist3(p(6), p(7), p(8), D(a(8)), D(a(9)), D(a(10)))
                                If s1 < bd Then
                                    s2 = s1 + CurveDist(edges(j), D(a(8)), D(a(9)), D(a(10)), sc)
                                    If s2 < sc Then sc = s2
                                End If
                            End If
                            If sc < bd Then bd = sc: Set best = edges(j): bk = i & "_" & j
                        End If
                    Next
                End If
            Next
            If Not best Is Nothing And bd < thr Then
                If Not used.Exists(bk) Then
                    used(bk) = 1
                    If best.Select4(True, SelData(m, 1)) Then n = n + 1
                End If
            Else
                LogLine "  WARN edge " & a(1) & " not matched (best " & Format(bd * 1000, "0.000") & " mm)"
            End If
        Next
        LogLine "  edges matched by geometry: " & n & "/" & gEdges.Count
    End If
    If n = 0 And gBoxes.Count > 0 Then
        infl = 1.2 * size + 0.00001
        For i = 0 To UBound(bodies)
            edges = bodies(i).GetEdges
            If IsArray(edges) Then
                For j = 0 To UBound(edges)
                    If EdgePts(edges(j), p) Then
                        For Each it In gBoxes
                            bx = Split(it, "|")
                            inb = True
                            For k = 0 To 2
                                If p(k) < D(bx(1 + k)) - infl Or p(k) > D(bx(4 + k)) + infl Then inb = False
                                If p(3 + k) < D(bx(1 + k)) - infl Or p(3 + k) > D(bx(4 + k)) + infl Then inb = False
                                If p(6 + k) < D(bx(1 + k)) - infl Or p(6 + k) > D(bx(4 + k)) + infl Then inb = False
                            Next
                            If inb Then
                                If edges(j).Select4(True, SelData(m, 1)) Then n = n + 1
                                Exit For
                            End If
                        Next
                    End If
                Next
            End If
        Next
        LogLine "  edges picked by blend-face boxes: " & n
    End If
    Err.Clear
    SelectBlendEdges = n
End Function

Sub OpFillet(ByVal m As Object, ByVal a As Variant)
    On Error Resume Next
    Dim nm As String, r As Double, f As Object, n As Long, vE As Variant
    nm = a(1): r = D(a(2))
    n = SelectBlendEdges(m, r)
    If n = 0 Then
        LogLine "FAIL " & nm & " fillet r=" & r & ": no edges selected": nFail = nFail + 1
        LogVolume m
        Exit Sub
    End If
    Set f = m.FeatureManager.FeatureFillet3(195, r, 0, 0, 0, 0, 0, vE, vE, vE, vE, vE, vE, vE)
    LogErr "FeatureFillet3"
    If f Is Nothing Then
        If m.FeatureFillet(195, r, 0, 0, vE, vE, vE) Then Set f = m.FeatureByPositionReverse(0)
        LogErr "FeatureFillet"
    End If
    Report m, f, nm, "fillet r=" & r & " edges=" & n
    m.ClearSelection2 True
End Sub

Sub OpChamfer(ByVal m As Object, ByVal a As Variant)
    On Error Resume Next
    Dim nm As String, typ As Long, d1 As Double, ang As Double, d2 As Double, f As Object, n As Long
    nm = a(1): typ = CLng(D(a(2))): d1 = D(a(3)): ang = D(a(4)): d2 = D(a(5))
    n = SelectBlendEdges(m, d1)
    If n = 0 Then
        LogLine "FAIL " & nm & " chamfer d=" & d1 & ": no edges selected": nFail = nFail + 1
        LogVolume m
        Exit Sub
    End If
    Set f = m.FeatureManager.InsertFeatureChamfer(4, typ, d1, ang, d2, 0, 0, 0)
    LogErr "InsertFeatureChamfer"
    Report m, f, nm, "chamfer type=" & typ & " d=" & d1 & " edges=" & n
    m.ClearSelection2 True
End Sub

' ---------------------------------------------------------------------------- mirror / patterns
Sub OpMirror(ByVal m As Object, ByVal a As Variant)
    On Error Resume Next
    Dim nm As String, pl As String, isBody As Boolean, s As Variant, f As Object, bodies As Variant, i As Long
    nm = a(1): pl = a(2): isBody = B(a(3))
    m.ClearSelection2 True
    If Not m.Extension.SelectByID2(pl, "PLANE", 0, 0, 0, False, 2, Nothing, 0) Then LogLine "  WARN mirror plane missing: " & pl
    If isBody Then
        bodies = m.GetBodies2(0, True)
        If IsArray(bodies) Then
            For i = 0 To UBound(bodies)
                bodies(i).Select2 True, SelData(m, 256)
            Next
        End If
        LogErr "select bodies"
        Set f = m.FeatureManager.InsertMirrorFeature2(True, False, True, False, 0)
        LogErr "InsertMirrorFeature2(body)"
    Else
        For Each s In Split(a(4), ";")
            If Not m.Extension.SelectByID2(CStr(s), "BODYFEATURE", 0, 0, 0, True, 1, Nothing, 0) Then LogLine "  WARN mirror seed missing: " & s
        Next
        Set f = m.FeatureManager.InsertMirrorFeature2(False, False, False, False, 0)
        LogErr "InsertMirrorFeature2"
    End If
    Report m, f, nm, "mirror about " & pl & IIf(isBody, " (body)", " of " & a(4))
    m.ClearSelection2 True
End Sub

Sub OpMirrorPart(ByVal m As Object, ByVal a As Variant)
    ' derived mirror part: the source part was rebuilt above; mirror its body about the plane (no merge),
    ' then delete the original body so only the mirrored (opposite-hand) body remains
    On Error Resume Next
    Dim nm As String, pl As String, f As Object, bodies As Variant, i As Long, f2 As Object
    nm = a(1): pl = a(2)
    m.ClearSelection2 True
    If Not m.Extension.SelectByID2(pl, "PLANE", 0, 0, 0, False, 2, Nothing, 0) Then LogLine "  WARN mirror plane missing: " & pl
    bodies = m.GetBodies2(0, True)
    If IsArray(bodies) Then
        For i = 0 To UBound(bodies)
            bodies(i).Select2 True, SelData(m, 256)
        Next
    End If
    LogErr "select bodies"
    Set f = m.FeatureManager.InsertMirrorFeature2(True, False, False, False, 0)
    LogErr "InsertMirrorFeature2(body, no merge)"
    If Not f Is Nothing And IsArray(bodies) Then
        m.ClearSelection2 True
        For i = 0 To UBound(bodies)
            bodies(i).Select2 True, Nothing
        Next
        Set f2 = m.FeatureManager.InsertDeleteBody2(False)
        LogErr "InsertDeleteBody2(original)"
        If f2 Is Nothing Then LogLine "  WARN original body not deleted: delete it by hand (Insert > Features > Delete/Keep Body)"
    End If
    Report m, f, nm, "mirror part about " & pl
    m.ClearSelection2 True
End Sub

Function SelSeeds(ByVal m As Object, ByVal seeds As String, ByVal mark As Long) As Long
    Dim s As Variant, n As Long
    For Each s In Split(seeds, ";")
        If m.Extension.SelectByID2(CStr(s), "BODYFEATURE", 0, 0, 0, True, mark, Nothing, 0) Then
            n = n + 1
        Else
            LogLine "  WARN pattern seed missing: " & s
        End If
    Next
    SelSeeds = n
End Function

Function VolOK(ByVal m As Object) As Boolean
    Dim nb As Long, v As Double
    VolOK = True
    If gExpect <= 0 Or gExpectTag <> "OK" Then Exit Function
    v = TotalVolume(m, nb)
    VolOK = Abs(v - gExpect) <= 0.005 * gExpect
End Function

Sub OpCPattern(ByVal m As Object, ByVal a As Variant)
    On Error Resume Next
    Dim nm As String, n As Long, ang As Double, eq As Boolean, seeds As String, axn As String, f As Object, tryN As Integer, rev As Boolean, pass As Integer
    nm = a(1): n = CLng(D(a(2))): ang = D(a(3)): eq = B(a(4)): seeds = a(5)
    axn = Axis2P(m, nm & "_axis", D(a(6)), D(a(7)), D(a(8)), D(a(9)), D(a(10)), D(a(11)))
    For pass = 0 To 1
        rev = (pass = 1)
        For tryN = 1 To 3
            m.ClearSelection2 True
            If axn <> "" Then m.Extension.SelectByID2 axn, "AXIS", 0, 0, 0, False, 1, Nothing, 0
            SelSeeds m, seeds, 4
            Select Case tryN
                Case 1: Set f = m.FeatureManager.FeatureCircularPattern5(n, ang, rev, "NULL", False, eq, False, False, False, False, 1, 0, "NULL", False)
                Case 2: Set f = m.FeatureManager.FeatureCircularPattern4(n, ang, rev, "NULL", False, eq, False)
                Case 3: Set f = m.FeatureManager.FeatureCircularPattern3(n, ang, rev, "NULL", False, eq)
            End Select
            LogErr "FeatureCircularPattern try " & tryN
            If Not f Is Nothing Then Exit For
        Next
        If f Is Nothing Then Exit For
        If VolOK(m) Or pass = 1 Then Exit For
        LogLine "  volume off replay -> retry reversed"
        DelFeature m, f
        Set f = Nothing
    Next
    Report m, f, nm, "circular x" & n & " angle=" & Format(ang * 57.2957795130823, "0.0") & " equal=" & eq & " rev=" & rev & " seeds " & seeds
    m.ClearSelection2 True
End Sub

Sub OpLPattern(ByVal m As Object, ByVal a As Variant)
    On Error Resume Next
    Dim nm As String, n1 As Long, s1 As Double, n2 As Long, s2 As Double, seeds As String, ax1 As String, ax2 As String
    Dim f As Object, pass As Integer, fl As Boolean
    nm = a(1): n1 = CLng(D(a(2))): s1 = D(a(3)): n2 = CLng(D(a(7))): s2 = D(a(8)): seeds = a(12)
    ax1 = Axis2P(m, nm & "_dir1", 0, 0, 0, D(a(4)), D(a(5)), D(a(6)))
    If n2 > 1 Then ax2 = Axis2P(m, nm & "_dir2", 0, 0, 0, D(a(9)), D(a(10)), D(a(11)))
    If n2 < 1 Then n2 = 1
    If s2 <= 0 Then s2 = s1
    For pass = 0 To 1
        fl = (pass = 1)
        m.ClearSelection2 True
        If ax1 <> "" Then m.Extension.SelectByID2 ax1, "AXIS", 0, 0, 0, False, 1, Nothing, 0
        If ax2 <> "" Then m.Extension.SelectByID2 ax2, "AXIS", 0, 0, 0, True, 2, Nothing, 0
        SelSeeds m, seeds, 4
        Set f = m.FeatureManager.FeatureLinearPattern5(n1, s1, n2, s2, fl, fl, "", "", False, False, False, False, False, False, False, False, False, False, 0, 0, False, False)
        LogErr "FeatureLinearPattern5"
        If f Is Nothing Then Exit For
        If VolOK(m) Or pass = 1 Then Exit For
        LogLine "  volume off replay -> retry flipped"
        DelFeature m, f
        Set f = Nothing
    Next
    Report m, f, nm, "linear " & n1 & "x" & n2 & " s=" & s1 & "/" & s2 & " flip=" & fl & " seeds " & seeds
    m.ClearSelection2 True
End Sub

Sub OpLoft(ByVal m As Object, ByVal a As Variant)
    On Error Resume Next
    Dim nm As String, isCut As Boolean, p As Variant, f As Object, first As Boolean
    nm = a(1): isCut = B(a(2))
    m.ClearSelection2 True
    first = True
    For Each p In Split(a(3), ";")
        If Not m.Extension.SelectByID2(CStr(p), "SKETCH", 0, 0, 0, Not first, 1, Nothing, 0) Then LogLine "  WARN loft profile missing: " & p
        first = False
    Next
    If isCut Then
        Set f = m.FeatureManager.InsertCutBlend(False, True, False, 1, 0, 0, False, 0, 0, 0, True, True)
        LogErr "InsertCutBlend"
    Else
        Set f = m.FeatureManager.InsertProtrusionBlend(False, True, False, 1, 0, 0, 1, 1, True, True, False, 0, 0, 0, True, True, True)
        LogErr "InsertProtrusionBlend"
        If f Is Nothing Then
            If m.FeatureByPositionReverse(0).GetTypeName2 = "Blend" Then Set f = m.FeatureByPositionReverse(0)
        End If
    End If
    Report m, f, nm, IIf(isCut, "loft cut", "loft") & " through " & a(3) & " (no guide curves)"
    m.ClearSelection2 True
End Sub

Sub OpSuppress(ByVal m As Object, ByVal a As Variant)
    On Error Resume Next
    m.ClearSelection2 True
    If m.Extension.SelectByID2(a(1), "BODYFEATURE", 0, 0, 0, False, 0, Nothing, 0) Then
        m.EditSuppress2
        LogErr "EditSuppress2"
        LogLine "  suppressed " & a(1) & " (suppressed in the original)"
    Else
        LogLine "  WARN cannot select " & a(1) & " to suppress"
    End If
    m.ClearSelection2 True
End Sub

' ---------------------------------------------------------------------------- dispatcher
Sub ExecOp(ByVal m As Object, ByVal raw As String)
    On Error Resume Next
    Dim a As Variant
    If Len(raw) = 0 Then Exit Sub
    If Left(raw, 1) = "#" Then Exit Sub
    a = Split(raw, "|")
    Select Case a(0)
        Case "PART": LogLine "PART " & a(1)
        Case "FINAL": gFinalReplay = D(a(1)): gFinalMass = D(a(2)): gFinalKg = D(a(3))
        Case "REFPLANE": OpRefPlane m, a
        Case "SKETCH": OpSketch m, a, raw
        Case "SKFRAME": OpFrame m, a
        Case "LINE": OpLine m, a
        Case "ARC": OpArc m, a
        Case "CIRCLE": OpCircle m, a
        Case "SPLINE": OpSpline m, a
        Case "POINT": OpPoint m, a
        Case "MERGE": OpMerge m, a
        Case "REL": OpRel m, a
        Case "DIM": OpDim m, a
        Case "CONTOUR": OpContour a
        Case "ENDSKETCH": OpEndSketch m, a
        Case "EXPECT": gExpect = D(a(1)): gExpectTag = a(2)
        Case "UPTO": gUpto.Add raw
        Case "EDGE": gEdges.Add raw
        Case "EDGEBOX": gBoxes.Add raw
        Case "EXTRUDE": OpExtrude m, a: ClearPending
        Case "REVOLVE": OpRevolve m, a: ClearPending
        Case "FILLET": OpFillet m, a: ClearPending
        Case "CHAMFER": OpChamfer m, a: ClearPending
        Case "MIRROR": OpMirror m, a: ClearPending
        Case "MIRRORPART": OpMirrorPart m, a: ClearPending
        Case "CPATTERN": OpCPattern m, a: ClearPending
        Case "LPATTERN": OpLPattern m, a: ClearPending
        Case "LOFT": OpLoft m, a: ClearPending
        Case "SUPPRESS": OpSuppress m, a
        Case "SKIP": LogLine "SKIP " & a(1) & " (" & a(2) & "): " & a(3): nSkip = nSkip + 1
        Case Else: LogLine "  WARN unknown op " & a(0)
    End Select
    If Err.Number <> 0 Then LogLine "  ERR op " & a(0) & ": " & Err.Number & " " & Err.Description: Err.Clear
End Sub

Sub ClearPending()
    Set gEdges = New Collection
    Set gBoxes = New Collection
    Set gUpto = New Collection
End Sub

' rebuild one part from ops; returns True when the part was saved
Function RunPart(ByRef ops() As String, ByVal nOps As Long, ByVal outDir As String, ByVal partName As String) As Boolean
    Dim m As Object, tpl As String, i As Long, errs As Long, warns As Long, v As Double, nb As Long, outPath As String
    On Error Resume Next
    RunPart = False
    gPartName = partName
    logPath = outDir & partName & "_rebuild_log.txt"
    Kill logPath
    Err.Clear
    nOK = 0: nFail = 0: nSkip = 0: nWarn = 0: gExpect = 0: gFinalReplay = 0: gFinalMass = 0: gFinalKg = 0
    Set gAll = CreateObject("Scripting.Dictionary")
    Set gGeo = CreateObject("Scripting.Dictionary")
    Set gCont = CreateObject("Scripting.Dictionary")
    Set gFlip = CreateObject("Scripting.Dictionary")
    Set gFrame = CreateObject("Scripting.Dictionary")
    Set gSupport = CreateObject("Scripting.Dictionary")
    Set gSegs = CreateObject("Scripting.Dictionary")
    Set gSk = Nothing
    ClearPending
    LogLine "START " & partName & " (" & nOps & " ops)"
    tpl = swApp.GetUserPreferenceStringValue(8)
    Set m = swApp.NewDocument(tpl, 0, 0, 0)
    If m Is Nothing Then LogLine "FAIL NewDocument (template " & tpl & ")": Exit Function
    swApp.SetUserPreferenceToggle 10, False
    m.SketchManager.AddToDB = True
    m.SketchManager.DisplayWhenAdded = False
    For i = 0 To nOps - 1
        ExecOp m, ops(i)
    Next
    Err.Clear
    m.ClearSelection2 True
    m.ForceRebuild3 False
    HideRefs m
    m.ShowNamedView2 "*Isometric", 7
    m.ViewZoomtofit2
    outPath = outDir & partName & "_rebuilt.SLDPRT"
    m.Extension.SaveAs outPath, 0, 1, Nothing, errs, warns
    LogErr "SaveAs"
    LogLine "saved " & outPath & " errs=" & errs & " warns=" & warns
    v = TotalVolume(m, nb)
    LogLine "features OK=" & nOK & " FAIL=" & nFail & " SKIP=" & nSkip & " WARN=" & nWarn
    LogLine "final volume=" & Format(v * 1E+9, "0.0") & " mm3 bodies=" & nb & _
            "  replay=" & Format(gFinalReplay * 1E+9, "0.0") & " mm3  original(asm MASS)=" & Format(gFinalMass * 1E+9, "0.0") & " mm3" & _
            IIf(gFinalMass > 0, "  diff vs original=" & Format((v - gFinalMass) / gFinalMass * 100, "0.00") & "%", "")
    LogLine "DONE " & partName
    swApp.CloseDoc m.GetTitle
    Err.Clear
    RunPart = True
End Function

Function PickFolder(ByVal title As String, ByVal dflt As String) As String
    On Error Resume Next
    Dim sh As Object, fo As Object, s As String
    Set sh = CreateObject("Shell.Application")
    Set fo = sh.BrowseForFolder(0, title, 0)
    If Not fo Is Nothing Then s = fo.Self.Path
    Err.Clear
    If s = "" Then s = InputBox(title, "sw_gen rebuild", dflt)
    If s <> "" And Right(s, 1) <> "\" Then s = s & "\"
    PickFolder = s
End Function
