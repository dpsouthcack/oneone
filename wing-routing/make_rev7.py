import json, re, sys
src, dst = sys.argv[1], sys.argv[2]
raw = open(src, 'rb').read().decode()
def dump(o): return re.sub(r'e([+-])0(\d)', r'e\1\2', json.dumps(o, indent=2, ensure_ascii=False)).replace('\n', '\r\n')
d = json.loads(raw); assert dump(d) == raw, 'round-trip not byte-identical'
a = d['ae_data']; lcl = a['io']['in']['LCL']
a['ch']['2']['name'] = 'LEAD MIC2'                       # A06: match port LCL 2 and ch 1 "LEAD MIC1"
for n in ('3', '4', '5'): lcl[n]['name'] = 'MIC' + n     # A06: "MIC 3/4/5" -> "MIC3/4/5" (matches ch names, MIC6-8 style)
open(dst, 'wb').write(dump(d).encode())
