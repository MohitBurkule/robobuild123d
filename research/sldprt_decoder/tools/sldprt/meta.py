"""Keywords feature tree + document property / material XML streams."""
import html
import re

SKIP_TYPES = {'Annotations', 'Surface Bodies', 'Ambient', 'Directional', 'SOLIDWORKS Materials', 'Lights',
              'Cameras', 'Sensors', 'Comments', 'Favorites', 'History', 'Selection Sets', 'Equations',
              'Origin', 'Material', 'Notes', 'ConfigurationManager', 'Lights and Cameras', 'Configuration', 'Markups', 'Exploded Views', 'Solid Bodies', 'Design Binder'}


def _text(b):
    if b[:2] in (b'\xff\xfe', b'\xfe\xff'):
        return b.decode('utf-16', 'replace')
    i = b.find(b'<')
    return b[max(i, 0):].decode('utf-8', 'replace')


def parse_keywords(xml):
    items = {}
    r = re.search(r'<Keywords[^>]*>', xml)
    if r:
        xml = xml[r.end():]
    for m in re.finditer(r'<(\w+) id="(\d+)"([^>]*?)(/>|>(.*?)</\1>)', xml, re.S):
        tag, fid, attrs, _, body = m.groups()
        a = dict(re.findall(r'(\w+)="([^"]*)"', attrs))
        a = {k: html.unescape(v) for k, v in a.items()}
        dims = [(n, html.unescape(v).strip()) for n, v in re.findall(r'<Dimension Name="([^"]+)">(.*?)</Dimension>', body or '', re.S)]
        items[int(fid)] = {'id': int(fid), 'tag': tag, 'name': a.get('Name', ''), 'type': a.get('Type', tag),
                           'attrs': a, 'dims': dims,
                           'children': [int(c) for c in re.findall(r'\d+', a.get('DissectableChildren', ''))]}
    return items


def sketch_parents(items):
    par = {}
    for i, it in items.items():
        for c in it['children']:
            par[c] = i
    return par


def parse_props(xml):
    props = dict((n, v) for n, v in re.findall(r'<property name="([^"]+)"[^>]*><vt:\w+>([^<]*)<', xml))
    out = {'properties': props}
    for k, v in props.items():
        if k.startswith('SW-MassProp'):
            nums = [float(x) for x in v.split(',') if x.strip()]
            labels = ['cog_x_m', 'cog_y_m', 'cog_z_m', 'volume_m3', 'surface_area_m2', 'mass_kg',
                      'inertia_1', 'inertia_2', 'inertia_3', 'inertia_4', 'inertia_5', 'inertia_6', 'unknown_a', 'unknown_b']
            out.setdefault('mass_props', {})[k] = {
                'raw': nums, 'interpretation': dict(zip(labels, nums))}
    return out


def parse_material(xml):
    out = {}
    m = re.search(r'<material name="([^"]+)"', xml)
    if m:
        out['name'] = m.group(1)
    for k, dn, v in re.findall(r'<(\w+) displayname="([^"]+)" value="([^"]+)"', xml):
        out[k] = {'displayname': dn, 'value': v}
    return out


def collect_meta(streams):
    meta = {'keywords': None, 'props': {}, 'material': {}, 'configs': [], 'xml_other': []}
    for s in streams:
        d = s['data']
        if b'<Keywords' in d[:4000]:
            meta['keywords'] = _text(d)
        elif b'SolidworksInformation-properties' in d[:400] or b'SW-MassProp' in d:
            meta['props'] = parse_props(_text(d))
        elif b'm\x00s\x00t\x00n\x00s\x00:\x00m\x00a\x00t' in d[:600] or b'mstns:materials' in d[:600]:
            meta['material'] = parse_material(_text(d))
        elif b'<swConfigurationList' in d or b'swConfiguration ' in d:
            t = _text(d)
            meta['configs'] = re.findall(r'<swConfiguration id="(\d+)" swName="([^"]*)"', t)
    return meta


def equations_from_text(texts):
    """Equation strings look like '"D1@Sketch1" = 12' (UTF-16 or ASCII)."""
    eqs = set()
    for t in texts:
        for m in re.finditer(r'"[^"\r\n]{1,60}"\s*=\s*[^\r\n"]{1,120}', t):
            eqs.add(m.group(0).strip())
    return sorted(eqs)
