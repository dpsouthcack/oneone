import json, re, sys
src, dst = sys.argv[1], sys.argv[2]
raw = open(src, 'rb').read().decode()
def dump(o): return re.sub(r'e([+-])0(\d)', r'e\1\2', json.dumps(o, indent=2, ensure_ascii=False)).replace('\n', '\r\n')
d = json.loads(raw); assert dump(d) == raw, 'round-trip not byte-identical'
a = d['ae_data']; io = a['io']
B = '12'; assert a['bus'][B]['name'] == 'IEM8'
a['bus'][B]['name'] = 'DJ+VID P16'                                   # DP: repurpose IEM8 as DJ+VIDEO P16 mix
assert not any(v['on'] for v in a['bus'][B]['main'].values())        # not on any main
for g in ('ch', 'aux'):
    for c in a[g].values():
        s = c['send'][B]
        if c['name'] in ('DJ', 'VIDEO'): s.update(on=True, lvl=0, mode='PRE')   # P16 feeds 0 dB PRE
        else: s['on'] = False
# unpatch every output carrying Bus 12 (BUS signals 23/24)
off = []
for g, ps in io['out'].items():
    for p, v in ps.items():
        if v['grp'] == 'BUS' and v['in'] in (23, 24): ps[p] = {'grp': 'OFF', 'in': 1}; off.append(f'{g}{p}')
# P16 slot 12 (A/B/C 44): User 12 -> Bus 12 POST L+R, outputs back on User 12
io['in']['USR']['12']['user'] = {'grp': 'BUS', 'in': 12, 'tap': 'POST', 'lr': 'L+R'}
for g in 'ABC':
    assert io['out'][g]['44'] == {'grp': 'OFF', 'in': 1}
    io['out'][g]['44'] = {'grp': 'USR', 'in': 12}
print('unpatched:', off)
open(dst, 'wb').write(dump(d).encode())
