#!/usr/bin/env python3
"""CLI: python3 -I decode_sldprt.py OUT_DIR file1.SLDPRT [...] [--step path.step]"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sldprt.decode import decode_file  # noqa: E402
from sldprt import report  # noqa: E402


def main(argv):
    step = None
    if '--step' in argv:
        k = argv.index('--step')
        step = argv[k + 1]
        argv = argv[:k] + argv[k + 2:]
    od, files = argv[0], argv[1:]
    os.makedirs(od, exist_ok=True)
    ents = None
    if step:
        from sldprt.stepcheck import load
        ents = load(step)
    for f in files:
        name = os.path.basename(f).rsplit('.', 1)[0]
        if f.upper().endswith('.SLDASM'):
            from sldprt import asm
            r = asm.decode_asm(f)
            if step:
                asm.check_against_step(r, asm.step_translations(step))
            open(os.path.join(od, name + '.mates.md'), 'w').write(asm.asm_md(r))
            open(os.path.join(od, name + '.mates.json'), 'w').write(report.to_json(r))
            print('ok %-45s components=%d mates=%d step=%s' % (name, len(r['components']), len(r['mates']), r.get('step_check')))
            continue
        try:
            r = decode_file(f, ents)
        except Exception as ex:  # keep batch going
            print('FAIL', name, repr(ex))
            continue
        open(os.path.join(od, name + '.faces.md'), 'w').write(report.faces_md(r))
        open(os.path.join(od, name + '.sketches.md'), 'w').write(report.sketches_md(r))
        open(os.path.join(od, name + '.json'), 'w').write(report.to_json(r))
        sc = r.get('step_check') or {}
        print('ok %-45s faces=%-4d sketches=%-3d ents=%-4d step=%s %s' % (
            name, len(r['faces']), len(r['sketches']), sum(len(s['entities']) for s in r['sketches']),
            sc.get('score'), sc.get('name')))


if __name__ == '__main__':
    main(sys.argv[1:])
