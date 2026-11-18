"""Extract input/output routing from a Behringer WING .snap (snapshot.11 JSON) into an xlsx workbook.
Usage: python3 wing_routing.py <file.snap> <out.xlsx>
Output-source index convention (inferred): BUS/MAIN 'in' numbers are L/R-interleaved signals,
i.e. BUS n -> Bus ceil(n/2) L (odd) / R (even). USR n -> User Signal n (definition in io.in.USR)."""
import json, sys, hashlib
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

snap, out = sys.argv[1], sys.argv[2]
raw = open(snap, 'rb').read(); d = json.loads(raw); a = d['ae_data']; io = a['io']
IN, OUT = io['in'], io['out']
busn = {int(k): v['name'] for k, v in a['bus'].items()}
mainn = {int(k): v['name'] for k, v in a['main'].items()}
mtxn = {int(k): v['name'] for k, v in a['mtx'].items()}
chn = {int(k): v['name'] for k, v in a['ch'].items()}
auxn = {int(k): v['name'] for k, v in a['aux'].items()}

def inname(g, i):
    p = IN.get(g, {}).get(str(i)); return (p or {}).get('name', '') if p else ''

def sig(grp, i):
    """Human label for an output/user source."""
    i = int(i)
    if grp == 'OFF': return 'OFF'
    if grp in ('BUS', 'MAIN'):
        n, side = (i + 1) // 2, 'L' if i % 2 else 'R'
        nm = (busn if grp == 'BUS' else mainn).get(n, '')
        return f"{'Bus' if grp=='BUS' else 'Main'} {n} {side} ({nm})"
    if grp == 'MTX': return f"Matrix {i} ({mtxn.get(i,'')})"
    if grp == 'USR': return f"User {i} = {usr(i)}"
    if grp == 'MON': return f"Monitor {i}"
    return f"{grp} in {i}" + (f" ({inname(grp,i)})" if inname(grp, i) else '')

def usr(i):
    u = IN['USR'][str(i)]['user']; g = u['grp']; n = u['in']
    if g == 'CH': s = f"Ch {n} ({chn.get(n,'')})"
    elif g == 'AUX': s = f"Aux {n} ({auxn.get(n,'') or 'unnamed'})"
    elif g == 'MTX': s = f"Matrix {n} ({mtxn.get(n,'')})"
    else: s = f"{g} in {n}" + (f" ({inname(g,n)})" if inname(g, n) else '')
    if 'tap' in u: s += f" {u['tap']} {u['lr']}"
    return s

wb = Workbook(); H = Font(bold=True, color='FFFFFF'); F = PatternFill('solid', fgColor='305496')
def sheet(title, header, rows, first=False):
    ws = wb.active if first else wb.create_sheet()
    ws.title = title; ws.append(header)
    for c in ws[1]: c.font = H; c.fill = F
    for r in rows: ws.append(r)
    for i, h in enumerate(header, 1):
        w = max([len(str(h))] + [len(str(r[i-1])) for r in rows if i-1 < len(r)])
        ws.column_dimensions[get_column_letter(i)].width = min(60, w + 2)
    ws.freeze_panes = 'A2'; return ws

# Channel input routing
rows = []
for grp, names in (('ch', chn), ('aux', auxn)):
    for k, c in a[grp].items():
        cn = c['in']['conn']; g, i = cn['grp'], cn['in']
        mode = IN.get(g, {}).get(str(i), {}).get('mode', '')
        ph = IN.get(g, {}).get(str(i), {}).get('vph', '')
        alt = f"{cn['altgrp']} {cn['altin']}" if cn['altgrp'] != 'OFF' else ''
        mains = ', '.join(f"M{m}({mainn[int(m)]}) {v['lvl']:.0f}dB" for m, v in c['main'].items() if v['on'])
        sends = ', '.join(f"{('MX'+s[2:]+'('+mtxn[int(s[2:])]+')') if s.startswith('MX') else ('B'+s+'('+busn[int(s)]+')')} {v['lvl']:.0f}dB {v.get('mode','')}".strip()
                          for s, v in c['send'].items() if v['on'] and v['lvl'] > -144)
        sends_inf = ', '.join(s for s, v in c['send'].items() if v['on'] and v['lvl'] <= -144)
        rows.append([f"{'CH' if grp=='ch' else 'AUX'} {k}", c['name'], f"{g} {i}", inname(g, i), mode, 'ON' if ph else '',
                     alt, 'MUTED' if c['mute'] else '', round(c['fdr'], 1), mains or 'none', sends or 'none', sends_inf])
sheet('Channel Inputs', ['Strip', 'Strip name', 'Source', 'Source port name', 'Port mode', '+48V', 'Alt source (altsw ' + str(io['altsw']) + ')',
                         'Mute', 'Fader dB', 'Main assigns (level)', 'Active sends (level/tap)', 'Sends ON but at -inf'], rows, first=True)

# Physical/console input ports with names
rows = []
for g, ports in IN.items():
    if g in ('USR', 'OSC'): continue
    for p, v in ports.items():
        if v.get('name') or v.get('vph') or v.get('g'):
            used = [s for s, c in [(f"CH {k}", c) for k, c in a['ch'].items()] + [(f"AUX {k}", c) for k, c in a['aux'].items()]
                    if c['in']['conn']['grp'] == g and c['in']['conn']['in'] == int(p)]
            rows.append([g, int(p), v.get('name', ''), v.get('mode', ''), v.get('g', ''), 'ON' if v.get('vph') else '', ', '.join(used)])
sheet('Input Ports', ['Group', 'Port', 'Name', 'Mode', 'Gain', '+48V', 'Patched to strip'], rows)

# Outputs
rows = []
for g, ports in OUT.items():
    for p, v in ports.items():
        if v['grp'] != 'OFF':
            rows.append([g, int(p), v['grp'], v['in'], sig(v['grp'], v['in'])])
sheet('Output Patch', ['Output group', 'Port', 'Source group', 'Source index', 'Source (decoded)'], rows)
off = {g: sum(1 for v in ports.values() if v['grp'] == 'OFF') for g, ports in OUT.items()}

# User signals
rows = [[int(k), usr(int(k)), ', '.join(f"{g} {p}" for g, ports in OUT.items() for p, v in ports.items() if v['grp'] == 'USR' and v['in'] == int(k))]
        for k in IN['USR']]
sheet('User Signals', ['User #', 'Definition', 'Feeds outputs'], rows)

# Buses / mains / matrices
rows = []
for k, b in a['bus'].items():
    rows.append([f"Bus {k}", b['name'], 'mono' if b['busmono'] else 'stereo', round(b['fdr'], 1), 'MUTED' if b['mute'] else '',
                 ', '.join(f"M{m}" for m, v in b['main'].items() if v['on']) or 'none', f"pre:{b['preins']['ins'] if b['preins']['on'] else '-'} post:{b['postins']['ins'] if b['postins']['on'] else '-'}"])
for k, b in a['main'].items():
    rows.append([f"Main {k}", b['name'], 'mono' if b['busmono'] else 'stereo', round(b['fdr'], 1), 'MUTED' if b['mute'] else '', '-',
                 f"pre:{b['preins']['ins'] if b['preins']['on'] else '-'} post:{b['postins']['ins'] if b['postins']['on'] else '-'}"])
for k, b in a['mtx'].items():
    rows.append([f"Matrix {k}", b['name'], 'mono' if b['busmono'] else 'stereo', round(b['fdr'], 1), 'MUTED' if b['mute'] else '', '-',
                 f"direct in: {b['dir']['in']}"])
sheet('Buses Mains Matrix', ['Bus', 'Name', 'Config', 'Fader dB', 'Mute', 'To mains', 'Inserts / notes'], rows)

# House rules (DP): never GRP taps; IEM sends always PRE
rr = []
def walk(o, path):
    if isinstance(o, dict):
        if o.get('mode') in ('GRP', 'PRE', 'POST') and 'lvl' in o:
            dest = path.split('.')[-1]; bname = '' if dest.startswith('MX') else busn.get(int(dest), '')
            if o['mode'] == 'GRP': rr.append(['R1 never GRP', path, bname, o['mode'], 'FAIL'])
            if bname.startswith('IEM') and o['mode'] != 'PRE': rr.append(['R2 IEM = PRE', path, bname, o['mode'], 'FAIL'])
        for k, v in o.items(): walk(v, path + '.' + k)
walk(a, 'ae')
if not rr: rr = [['R1 never GRP', 'all ch/aux sends', '', '-', 'PASS'], ['R2 IEM sends = PRE', 'all ch/aux sends to IEM buses', '', '-', 'PASS']]
sheet('Rule Checks', ['Rule', 'Send path', 'Destination', 'Tap', 'Result'], rr)
meta = [['Snapshot file', snap.split('/')[-1]], ['SHA-256', hashlib.sha256(raw).hexdigest()], ['Type', d['type']],
        ['Creator', f"{d['creator_name']} {d['creator_version']} ({d['creator_model']})"], ['Created', d['created']],
        ['Alt source switch', str(io['altsw'])], ['Monitor 1/2 source', ', '.join(v['src'] for v in a['cfg']['mon'].values())],
        ['Output ports OFF per group', ', '.join(f"{g}:{n}/{len(OUT[g])}" for g, n in off.items())],
        ['Index convention', 'BUS/MAIN output index is L/R interleaved (odd=L, even=R) — inferred from patch pattern, verify on console']]
sheet('Snapshot Info', ['Field', 'Value'], meta)
wb.save(out); print('saved', out)
