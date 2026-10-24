"""sw_gen: general SolidWorks rebuild-macro generator driven by SolidWorks API dumps.

    python3 -m sw_gen <part.dump.txt> [--refs <part.refs.txt>] [--no-replay] [--out DIR]
    python3 -m sw_gen --batch <dump dir> [--refs-dir DIR] [--out DIR]

Pipeline (each step is its own module):
    model    load the dump (rebuild_dump/dump_parser.py), refs.txt and assembly MASS lines
    sketch   per sketch: unique entity keys, merges, verified relations, dimensions, contours
    plan     feature list -> ops (ref planes, sketches, extrudes, revolves, blends, patterns, mirrors)
    replay   optional build123d replay of the ops: expected volume per step, blend edges, up-to faces
    emit     ops -> text lines; wraps them in the VBA interpreter (interp.bas) for a single-part macro
    batch    one VBA project that rebuilds every <part>.ops.txt found in a folder (resume-safe)
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REBUILD_DUMP = os.path.dirname(HERE)
SLDPRT = os.path.dirname(REBUILD_DUMP)
if REBUILD_DUMP not in sys.path:
    sys.path.insert(0, REBUILD_DUMP)

__all__ = ['HERE', 'REBUILD_DUMP', 'SLDPRT']
