import json, sys
def load(f): return json.load(open(f))['ae_data']
def members(a, mx):
    out = []
    for g in ('ch', 'aux', 'bus', 'main'):
        for n, c in a[g].items():
            v = c.get('send', {}).get(f'MX{mx}')
            if v and v['on']: out.append(f"{c['name'] or g+n}({v['lvl']:g}{' '+v['mode'] if 'mode' in v else (' pre' if v.get('pre') else ' post')})")
    return out
def slot(a, p):
    o = a['io']['out']['A'][str(p)]
    if o['grp'] == 'OFF': return 'OFF', ''
    if o['grp'] != 'USR': return f"{o['grp']} {o['in']}", ''
    u = a['io']['in']['USR'][str(o['in'])]['user']; g, i = u['grp'], u['in']
    nm = {'CH': lambda: a['ch'][str(i)]['name'], 'AUX': lambda: a['aux'][str(i)]['name'] or f'Aux {i}', 'MTX': lambda: a['mtx'][str(i)]['name']}.get(g, lambda: '')()
    src = f"U{o['in']}: {g} {i} {nm} {u.get('tap','')}".strip()
    mem = ', '.join(members(a, i)) if g == 'MTX' else ''
    return src, mem
O, N = load(sys.argv[1]), load(sys.argv[2])
same = all(O['io']['out'][g][str(p)] == O['io']['out']['A'][str(p)] for g in 'BC' for p in range(33, 49))
print('A/B/C 33-48 identical in original:', same, '| in rev12:', all(N['io']['out'][g][str(p)] == N['io']['out']['A'][str(p)] for g in 'BC' for p in range(33, 49)))
for s in range(1, 17):
    p = 32 + s; o, om = slot(O, p); n, nm = slot(N, p)
    print(f"P16 {s:2} (A/B/C {p}) | ORIGINAL: {o}" + (f"  <= {om or 'NO INPUTS'}" if o.startswith('U') and 'MTX' in o else ''))
    if (o, om) != (n, nm): print(f"{'':20}| REV12:    {n}" + (f"  <= {nm or 'NO INPUTS'}" if n.startswith('U') and 'MTX' in n else ''))
# any bus/main ever feeding a matrix?
print('bus/main->matrix sends ON (original):', [(g, n, k) for g in ('bus', 'main') for n, c in O[g].items() for k, v in c.get('send', {}).items() if v['on']])
print('matrix direct inputs (original):', {k: m['dir'] for k, m in O['mtx'].items() if m['dir']['in'] != 'OFF' or m['dir']['on']})
print('matrices on any output directly (original):', [(g, p, v) for g, ps in O['io']['out'].items() for p, v in ps.items() if v['grp'] == 'MTX'])
