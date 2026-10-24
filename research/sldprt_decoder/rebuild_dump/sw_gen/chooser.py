"""No-reference region choice from the SLDPRT itself: the tools/sldprt feature-stream decoder's
region chooser (moSketchChooser / region records, ~93% face-evidence agreement on the corpus).

sketch feature id -> set of dump segment keys ((type, 'index_pid')) bounding the selected regions,
or absent when the decoder has no chooser for that sketch (SolidWorks then uses the whole sketch).
"""
import os
import sys

from . import SLDPRT

TOOLS = os.path.join(SLDPRT, 'tools')
REVDEV = os.path.join(SLDPRT, 'revdev')


def sldprt_for(part_name):
    p = os.path.join(REVDEV, part_name + '.SLDPRT')
    return p if os.path.exists(p) else None


def selections(part_name, sketch_ids):
    """{sketch feature id: set((type, 'i_pid'))} for sketches whose region chooser decoded."""
    path = sldprt_for(part_name)
    if not path:
        return {}
    if TOOLS not in sys.path:
        sys.path.insert(0, TOOLS)
    try:
        from sldprt import fstream as FS
        from sldprt.validate import feature_stream
        d = feature_stream(path)
        if d is None:
            return {}
        dec = FS.decode(d, set())
    except Exception:
        return {}
    out = {}
    for fid in sketch_ids:
        X = dec.sketches.get(fid)
        if not X:
            continue
        sk = X['sketch']
        try:
            sel, has = FS.selected_serials(X['choosers'], X['regions'], sk, X['chains'] or None, faces=True)
        except Exception:
            continue
        if not has:
            continue
        inv = {}
        for s_ in sk.lines:
            inv[s_.serial] = (0, '%d_%d' % tuple(s_.api_id))
        for s_ in sk.arcs:
            inv[s_.serial] = (1, '%d_%d' % tuple(s_.api_id))
        out[fid] = {inv[x] for x in sel if x in inv}
    return out
