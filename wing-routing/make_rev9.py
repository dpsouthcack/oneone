import json, re, sys
src, dst = sys.argv[1], sys.argv[2]
raw = open(src, 'rb').read().decode()
def dump(o): return re.sub(r'e([+-])0(\d)', r'e\1\2', json.dumps(o, indent=2, ensure_ascii=False)).replace('\n', '\r\n')
d = json.loads(raw); assert dump(d) == raw, 'round-trip not byte-identical'
a = d['ae_data']
a['aux']['7']['name'] = 'CLICK'   # DP 2026-11-18: Aux 7 (C13-14) is click
a['aux']['8']['name'] = 'CUES'    # DP 2026-11-18: Aux 8 (C15-16) is cues
open(dst, 'wb').write(dump(d).encode())
