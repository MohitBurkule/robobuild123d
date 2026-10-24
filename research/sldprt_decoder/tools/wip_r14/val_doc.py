"""Round 14 (2): item_doc field decode vs the API DOC block of every A/B dump (+ macro truth for DOC/VIEW)."""
import sys, os, glob, re, json, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import item_doc as D
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../dumps_ab/')
PROPS = {316: [('TestProp', 'hello', 'text')], 317: [('TestProp', 'x' * 200, 'text')], 318: [('TestNum', '42', 'number')],
         319: [('TestDate', None, 'date')], 320: [('TestYes', 'Yes', 'yesno')], 321: [('TestProp', 'hello', 'text'), ('Second', 'world', 'text')],
         323: [('TestProp', 'hello', 'text')]}
tot = collections.defaultdict(lambda: [0, 0]); bad = collections.defaultdict(list)
def chk(k, ok, f, info=''):
    tot[k][0] += bool(ok); tot[k][1] += 1
    if not ok: bad[k].append((f, info))
for p in sorted(glob.glob(R + 'AB_*.SLDPRT')):
    f = os.path.basename(p)[:-7]; dp = p[:-7] + '.dump.txt'
    if not os.path.exists(dp): continue
    t = open(dp, errors='replace').read()
    if '\nDOC' not in t: continue
    doc = t.split('\nDOC', 1)[1]
    r = D.decode_file(p)
    cf = re.findall(r'^  CONFIG (.*)$', doc, re.M); ac = re.findall(r'^  ACTIVE_CONFIG (.*)$', doc, re.M)
    ds = re.findall(r'^  DISPLAY_STATE (.*)$', doc, re.M)
    mt = re.search(r'^  MATERIAL (.*?) db=(.*)$', doc, re.M); col = re.search(r'^  COLOUR (.*)$', doc, re.M)
    un = re.search(r'^  UNITS linear=(\d+) dec=(\d+)', doc, re.M); eq = re.findall(r'^  EQN (.*)$', doc, re.M)
    chk('CFG.names (set)', set(cf) == set(r['configurations']), f, (cf, r['configurations']))
    chk('CFG.active = first stored', ac and ac[0] == r['active_config'], f, (ac, r['active_config']))
    chk('CFG.display states (set)', set(ds) <= set(r['display_states']), f, (ds, r['display_states']))
    if mt:
        chk('MAT.name', (mt.group(1).strip() or None) == r['material'], f, (mt.group(1), r['material']))
        chk('MAT.db', (mt.group(2).strip() or None) == r['material_db'], f, (mt.group(2), r['material_db']))
    if col:
        v = [float(x) for x in col.group(1).strip(',').split(',')]
        v = [0.0 if abs(x) < 1e-300 else x for x in v]
        cands = [r['part_colour']] + [c['colour'] for c in r.get('config_visual', {}).values()]
        ok = any(c and all(abs(a - b) < (0.5 / 255 if i < 3 else 1e-6) for i, (a, b) in enumerate(zip(v, c))) for c in cands)
        chk('COLOUR.9 values (part or active config)', ok, f, (v, cands[:2]))
        chk('COLOUR.part block (moPart_c)', r['part_colour'] and all(abs(a - b) < (0.5 / 255 if i < 3 else 1e-6) for i, (a, b) in enumerate(zip(v, r['part_colour']))), f, (v, r['part_colour']))
    if un and r['units']:
        chk('UNITS.linear', int(un.group(1)) == r['units']['linear'], f, (un.group(1), r['units']))
        chk('UNITS.decimals', int(un.group(2)) == r['units']['decimals'], f, (un.group(2), r['units']))
    elif un: chk('UNITS.linear', False, f, 'none')
    chk('EQN.texts', [e.split(' = ')[0] + ' = ' + e.split(' = ')[1] for e in eq] == r['equations'][:len(eq)] and len(r['equations']) == len(eq), f, (eq, r['equations']))
    m = re.match(r'AB_DOC_(\d+)', f)
    if m:
        k = int(m.group(1))
        if k == 322:
            chk('DOC.config-specific prop', [(x['name'], x['value']) for x in r['config_props']] == [('CfgProp', 'cfg')], f, r['config_props'])
        else:
            want = PROPS[k]; got = r['custom_props']
            chk('DOC.prop names', [w[0] for w in want] == [g['name'] for g in got], f, got)
            chk('DOC.prop types', [w[2] for w in want] == [g['type'] for g in got], f, got)
            chk('DOC.prop values', all(w[1] is None or w[1] == g['value'] for w, g in zip(want, got)) and len(want) == len(got), f, got)
    elif not f.startswith('AB_CFG'):
        chk('DOC.no props when none set', not r['custom_props'], f, r['custom_props'])
    if f.startswith('AB_VIEW_351'): chk('VIEW.named view', r['views'] == ['MyView'], f, r['views'])
    elif f.startswith('AB_'): chk('VIEW.none', not r['views'], f, r['views'])
for k, (a, n) in sorted(tot.items()): print('%-45s %4d/%-4d %6.2f' % (k, a, n, 100 * a / n), bad[k][:2] if bad[k] else '')
json.dump({k: v for k, v in tot.items()}, open('val_doc.json', 'w'))
