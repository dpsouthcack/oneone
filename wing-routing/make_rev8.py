import json, re, sys
src, dst = sys.argv[1], sys.argv[2]
raw = open(src, 'rb').read().decode()
def dump(o): return re.sub(r'e([+-])0(\d)', r'e\1\2', json.dumps(o, indent=2, ensure_ascii=False)).replace('\n', '\r\n')
d = json.loads(raw); assert dump(d) == raw, 'round-trip not byte-identical'
a = d['ae_data']
# Ch 33-37 take A1-A5 = the alt (backup) sources of Ch 9-13; name after the primary channel + ALT
for n, prim in zip(range(33, 38), range(9, 14)):
    a['ch'][str(n)]['name'] = a['ch'][str(prim)]['name'] + ' ALT'
# Aux 1-6 named from their DCA assignment tag (#D8-#D13 = TRAX..TRAX-VOX); Aux 7-8 (no DCA) from their Ableton pair
dca = {k: v['name'] for k, v in a['dca'].items()}
for n in range(1, 9):
    c = a['aux'][str(n)]; t = [x[2:] for x in c['tags'].split(',') if x.startswith('#D')]
    if t: c['name'] = dca[t[0]]
    else:
        p = a['io']['in']['C'][str(c['in']['conn']['in'])]['name']      # e.g. C-ABLE13-14
        c['name'] = 'TRAX ' + p.split('ABLE')[1]
for g, ns in (('ch', range(33, 38)), ('aux', range(1, 9))):
    for n in ns: assert len(a[g][str(n)]['name']) <= 16, a[g][str(n)]['name']
open(dst, 'wb').write(dump(d).encode())
