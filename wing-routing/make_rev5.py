import json, re, sys
src, dst = sys.argv[1], sys.argv[2]
raw = open(src, 'rb').read().decode()
def dump(o): return re.sub(r'e([+-])0(\d)', r'e\1\2', json.dumps(o, indent=2, ensure_ascii=False)).replace('\n', '\r\n')
d = json.loads(raw); assert dump(d) == raw, 'round-trip not byte-identical'
a = d['ae_data']
# A04: sends already switched ON to Stage Mon 1-4 (Bus 1-4, PRE) and FX 13-16 (POST) raised -inf -> -10 dB,
# matching the IEM send level. Taps untouched; sends that are OFF (talkback ch 29-32) stay off.
for g in ('ch', 'aux'):
    for c in a[g].values():
        for b in ('1', '2', '3', '4', '13', '14', '15', '16'):
            s = c['send'][b]
            if s['on'] and s['lvl'] <= -144: s['lvl'] = -10
open(dst, 'wb').write(dump(d).encode())
