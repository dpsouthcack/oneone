import json, re, sys
src, dst = sys.argv[1], sys.argv[2]
raw = open(src, 'rb').read().decode()
def dump(o): return re.sub(r'e([+-])0(\d)', r'e\1\2', json.dumps(o, indent=2, ensure_ascii=False)).replace('\n', '\r\n')
d = json.loads(raw); assert dump(d) == raw, 'round-trip not byte-identical'
io = d['ae_data']['io']
io['in']['USR']['24']['user'] = {'grp': 'CH', 'in': 8, 'tap': 'PRE', 'lr': 'L+R'}   # USB 8: Ch7 R dup -> Ch 8 MIC8 PRE
io['out']['USB']['45'] = {'grp': 'LCL', 'in': 21}                                  # USB 45: B19 (blank) -> VIDEO L
io['out']['USB']['46'] = {'grp': 'LCL', 'in': 22}                                  # USB 46: B20 (blank) -> VIDEO R
open(dst, 'wb').write(dump(d).encode())
