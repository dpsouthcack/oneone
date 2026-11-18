import json, re, sys
src, dst = sys.argv[1], sys.argv[2]
raw = open(src, 'rb').read().decode()
def dump(o): return re.sub(r'e([+-])0(\d)', r'e\1\2', json.dumps(o, indent=2, ensure_ascii=False)).replace('\n', '\r\n')
d = json.loads(raw); assert dump(d) == raw, 'round-trip not byte-identical'
for b in d['ae_data']['bus'].values():          # A15: STAGE MON1-4 masters to 0 dB (selected by name)
    if b['name'].upper().startswith('STAGE MON'): b['fdr'] = 0
open(dst, 'wb').write(dump(d).encode())
