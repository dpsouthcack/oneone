import json, re, sys, copy
src, dst = sys.argv[1], sys.argv[2]
raw = open(src, 'rb').read().decode()
def dump(o): return re.sub(r'e([+-])0(\d)', r'e\1\2', json.dumps(o, indent=2, ensure_ascii=False)).replace('\n', '\r\n')
d = json.loads(raw); assert dump(d) == raw, 'round-trip not byte-identical'
a = d['ae_data']
ref = a['ch']['6']['send']['MX6']; assert ref['on'] and ref['mode'] == 'PRE'
a['ch']['7']['send']['MX6'] = copy.deepcopy(ref)        # DP: MIC7 into MICS P16, same settings as MIC3-6/8
open(dst, 'wb').write(dump(d).encode())
