import json, re, sys, copy
src, dst = sys.argv[1], sys.argv[2]
raw = open(src, 'rb').read().decode()
def dump(o): return re.sub(r'e([+-])0(\d)', r'e\1\2', json.dumps(o, indent=2, ensure_ascii=False)).replace('\n', '\r\n')
d = json.loads(raw)
assert dump(d) == raw, 'round-trip not byte-identical'
a = d['ae_data']
a['main']['1']['fdr'] = 0                      # A02: HOUSE to unity, matching Mains 2-4
for g in ('ch', 'aux'):                         # A03: IEM5-8 (bus 9-12) mirror IEM1-4 (bus 5-8)
    for n, c in a[g].items():
        for src_b, dst_b in ((5, 9), (6, 10), (7, 11), (8, 12)):
            c['send'][str(dst_b)] = copy.deepcopy(c['send'][str(src_b)])
open(dst, 'wb').write(dump(d).encode())
