import json, re, sys
src, dst = sys.argv[1], sys.argv[2]
raw = open(src, 'rb').read().decode()
def dump(o): return re.sub(r'e([+-])0(\d)', r'e\1\2', json.dumps(o, indent=2, ensure_ascii=False)).replace('\n', '\r\n')
d = json.loads(raw); assert dump(d) == raw, 'round-trip not byte-identical'
a = d['ae_data']
# Matrix 4 XTRA P16 had no inputs (verified) and feeds P16 slot 11 via User 11 -> becomes CLICK/CUES P16 channel
assert not any(c.get('send', {}).get('MX4', {}).get('on') for g in ('ch', 'aux', 'bus', 'main') for c in a[g].values())
a['mtx']['4']['name'] = 'CLK+CUE P16'
for c in a['aux'].values():
    if c['name'] in ('CLICK', 'CUES'):
        c['main']['4']['on'] = False                                   # DP: never to STREAM
        c['send']['MX5']['on'] = False                                 # out of ABLETON P16 (slot 13)
        c['send']['MX4'].update(on=True, lvl=0, mode='PRE')            # into own P16 channel (slot 11), PRE like other P16 feeds
open(dst, 'wb').write(dump(d).encode())
