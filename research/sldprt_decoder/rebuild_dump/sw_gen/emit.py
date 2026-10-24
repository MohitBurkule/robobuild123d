"""ops -> text: <part>.ops.txt (data for the batch macro) and <part>_rebuild.txt (single-part macro =
interpreter + embedded ops)."""
from __future__ import annotations
import os

from . import HERE

INTERP = os.path.join(HERE, 'interp.bas')
CHUNK = 300          # AddOp lines per Sub (VBA 64 KB per procedure)


def op_lines(planner, header=()):
    out = list(header)
    for fp in planner.plans:
        out.append(f'# {fp.name} ({fp.type}) {fp.status} {fp.reason}'.replace('\n', ' ')[:900])
        out += [o.line() for o in fp.ops]
    return out


def _vba_str(s):
    return '"' + s.replace('"', '""') + '"'


def _split_long(s, width=800):
    """VBA lines are limited to 1023 chars: break long string literals with & _ continuation."""
    parts = [s[i:i + width] for i in range(0, len(s), width)] or ['']
    return ' & _\n        '.join(_vba_str(p) for p in parts)


def single_macro(part_name, lines):
    interp = open(INTERP, encoding='utf-8').read()
    subs, calls = [], []
    for i in range(0, len(lines), CHUNK):
        n = i // CHUNK
        body = '\n'.join(f'    AddOp {_split_long(l)}' for l in lines[i:i + CHUNK])
        subs.append(f'Sub LoadOps{n}()\n{body}\nEnd Sub\n')
        calls.append(f'    LoadOps{n}')
    safe = part_name.replace('"', "'")
    head = f"""' {safe} - rebuilt from its SolidWorks API dump by rebuild_dump/sw_gen (python3 -m sw_gen).
' Paste into a new macro (Tools > Macro > New), press F5 and pick the output folder.
' Writes <output>\\{safe}_rebuilt.SLDPRT and {safe}_rebuild_log.txt (OK/FAIL/SKIP per feature + volumes).
Option Explicit
Dim gOps() As String
Dim gN As Long
"""
    main = f"""
Sub AddOp(ByVal s As String)
    If gN > UBound(gOps) Then ReDim Preserve gOps(UBound(gOps) * 2 + 1)
    gOps(gN) = s
    gN = gN + 1
End Sub

Sub main()
    Dim outDir As String
    Set swApp = Application.SldWorks
    Set mu = swApp.GetMathUtility
    gShow = True
    outDir = PickFolder("Folder for {safe}_rebuilt.SLDPRT and the log", Environ("USERPROFILE") & "\\Desktop")
    If outDir = "" Then Exit Sub
    ReDim gOps(1023): gN = 0
{chr(10).join(calls)}
    RunPart gOps, gN, outDir, {_vba_str(safe)}
    MsgBox "{safe}: " & nOK & " OK, " & nFail & " failed, " & nSkip & " skipped." & vbCrLf & "Log: " & logPath
End Sub
"""
    return head + interp + main + '\n' + '\n'.join(subs)


def batch_macro():
    interp = open(INTERP, encoding='utf-8').read()
    head = """' sw_gen BATCH rebuild: rebuilds every <part>.ops.txt in a folder (one part document at a time).
' Paste into a new macro (Tools > Macro > New) with NO part open, press F5, pick the ops folder,
' then the output folder. Per part: <part>_rebuilt.SLDPRT + <part>_rebuild_log.txt.
' Resume-safe: parts whose log ends with DONE are skipped; a part that was STARTed but never finished
' (SolidWorks crashed on it) is skipped too and listed in batch_summary.txt - delete its log to retry.
Option Explicit
"""
    main = r"""
Function ReadOps(ByVal path As String, ByRef ops() As String) As Long
    Dim fn As Integer, s As String, n As Long
    ReDim ops(1023)
    fn = FreeFile
    Open path For Input As #fn
    Do While Not EOF(fn)
        Line Input #fn, s
        If n > UBound(ops) Then ReDim Preserve ops(UBound(ops) * 2 + 1)
        ops(n) = s
        n = n + 1
    Loop
    Close #fn
    ReadOps = n
End Function

Function LogState(ByVal path As String) As String
    ' "" no log | "DONE" | "STARTED"
    Dim fn As Integer, s As String, st As String
    On Error Resume Next
    LogState = ""
    If Dir(path) = "" Then Exit Function
    fn = FreeFile
    Open path For Input As #fn
    Do While Not EOF(fn)
        Line Input #fn, s
        If InStr(s, "  DONE ") > 0 Then st = "DONE" Else If st = "" And InStr(s, "  START ") > 0 Then st = "STARTED"
    Loop
    Close #fn
    LogState = st
End Function

Sub Summary(ByVal outDir As String, ByVal s As String)
    Dim fn As Integer
    fn = FreeFile
    Open outDir & "batch_summary.txt" For Append As #fn
    Print #fn, Format(Now, "yyyy-mm-dd hh:nn:ss") & "  " & s
    Close #fn
End Sub

Sub main()
    Dim opsDir As String, outDir As String, f As String, names As New Collection, nm As Variant, ops() As String, n As Long
    Dim st As String, done As Long, skipped As Long
    Set swApp = Application.SldWorks
    Set mu = swApp.GetMathUtility
    gShow = False
    opsDir = PickFolder("Folder with the .ops.txt files (deliver\rebuild_macros\ops)", Environ("USERPROFILE") & "\Desktop\ops")
    If opsDir = "" Then Exit Sub
    outDir = PickFolder("Output folder for rebuilt parts and logs", Environ("USERPROFILE") & "\Desktop\rebuilt")
    If outDir = "" Then Exit Sub
    f = Dir(opsDir & "*.ops.txt")
    Do While f <> ""
        names.Add Left(f, Len(f) - 8)
        f = Dir()
    Loop
    Summary outDir, "batch start: " & names.Count & " parts from " & opsDir
    For Each nm In names
        st = LogState(outDir & nm & "_rebuild_log.txt")
        If st = "DONE" Then
            Summary outDir, "skip (done earlier) " & nm
            skipped = skipped + 1
        ElseIf st = "STARTED" Then
            Summary outDir, "skip (crashed earlier - delete its log to retry) " & nm
            skipped = skipped + 1
        Else
            n = ReadOps(opsDir & nm & ".ops.txt", ops)
            RunPart ops, n, outDir, CStr(nm)
            Summary outDir, nm & ": OK=" & nOK & " FAIL=" & nFail & " SKIP=" & nSkip & " WARN=" & nWarn
            done = done + 1
        End If
    Next
    Summary outDir, "batch end: built " & done & ", skipped " & skipped
    MsgBox "Batch done: built " & done & ", skipped " & skipped & "." & vbCrLf & "See " & outDir & "batch_summary.txt"
End Sub
"""
    return head + interp + main
