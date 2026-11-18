import json, re, sys, copy
src, dst = sys.argv[1], sys.argv[2]
raw = open(src, 'rb').read().decode()
def dump(o): return re.sub(r'e([+-])0(\d)', r'e\1\2', json.dumps(o, indent=2, ensure_ascii=False)).replace('\n', '\r\n')
d = json.loads(raw); assert dump(d) == raw, 'round-trip not byte-identical'
a = d['ae_data']; out = a['io']['out']
# DP: MIC8 no own P16 slot; slot 12 empty. Slot 12 = User 12 on A44/B44/C44 -> switch those outputs OFF (proven format).
for g in ('A', 'B', 'C'):
    assert out[g]['44'] == {'grp': 'USR', 'in': 12}
    out[g]['44'] = {'grp': 'OFF', 'in': 1}
# DP: MIC8 joins MICS P16 (Matrix 6) with the same send settings as MIC3-6
ref = a['ch']['6']['send']['MX6']; assert ref['on'] and ref['mode'] == 'PRE'
a['ch']['8']['send']['MX6'] = copy.deepcopy(ref)
open(dst, 'wb').write(dump(d).encode())
