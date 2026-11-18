import json, re, sys
src, dst = sys.argv[1], sys.argv[2]
raw = open(src, 'rb').read().decode()
def dump(o): return re.sub(r'e([+-])0(\d)', r'e\1\2', json.dumps(o, indent=2, ensure_ascii=False)).replace('\n', '\r\n')
d = json.loads(raw); assert dump(d) == raw, 'round-trip not byte-identical'
a = d['ae_data']
mains = {k: m['name'] for k, m in a['main'].items()}
buses = {k: b['name'] for k, b in a['bus'].items()}
HOUSE_MAINS = {'HOUSE', 'SUBS', 'DELAY'}                               # PA mains
FLOOR = {k for k, n in buses.items() if n.startswith('STAGE MON')}     # floor wedges
FXB = {k for k, b in a['bus'].items() if b['main'].get('1', {}).get('on') and not b['name'].startswith(('STAGE', 'IEM'))}  # FX buses feeding HOUSE
for c in a['aux'].values():
    if c['name'] in ('CLICK', 'CUES'):                                 # DP rule: click/cues never in house or floor monitors
        for k, m in c['main'].items():
            if mains[k] in HOUSE_MAINS: m['on'] = False
        for k in FLOOR | FXB: c['send'][k]['on'] = False
print('floor', sorted(FLOOR, key=int), 'fx->house', sorted(FXB, key=int))
open(dst, 'wb').write(dump(d).encode())
