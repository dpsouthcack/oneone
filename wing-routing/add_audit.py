import sys, openpyxl
from openpyxl.styles import Font, PatternFill
p = sys.argv[1]; wb = openpyxl.load_workbook(p)
H = Font(bold=True, color='FFFFFF'); F = PatternFill('solid', fgColor='C00000')
flags = [
 ('A01','High — RESOLVED rev1','[RESOLVED 2026-11-18 in DPSC_2026_DEFAULT_1A_rev1: User 13 (P16 slot 13 on A/B/C 45) changed from Aux 1 PRE to Matrix 5 POST L+R] Matrix 5 "ABLETON P16" is fed (Aux 1-8 send to MX5 at 0 dB) but no User Signal or output carries Matrix 5. USR 1-16 cover MTX 1,2,3,4,6,7,8 only.','io.in.USR 1-16; aux.*.send.MX5','Assign a user signal / P16 slot to Matrix 5 if Ableton is wanted on personal mixers.'),
 ('A02','High','Main 1 HOUSE fader is at -inf (-144 dB) in this scene, while Mains 2-4 are at 0 dB.','main.1.fdr = -144','Confirm intended (safe default) before show.'),
 ('A03','High','IEM5-IEM8 (Buses 9-12) are patched to A/B/C outputs but no channel or aux sends to them.','ch/aux send 9-12 all off; out A5-8, B5-8, C5-8, C17-24','Build IEM5-8 mixes or unpatch.'),
 ('A04','Med','Stage Mon 1-4 (Buses 1-4) and FX buses 13-16 have sends switched ON but at -inf on every channel; only IEM1-4 (Buses 5-8) carry signal (-10 dB PRE).','ch.*.send 1-4,13-16 lvl -144','Expected for a template; note no FX returns or wedges will sound until raised.'),
 ('A05','Med — RESOLVED rev1','[RESOLVED 2026-11-18 in rev1: LCL 6 renamed MIC8 -> MIC6] Input port LCL 6 is labelled "MIC8" (duplicate of LCL 8 "MIC8"); channel 6 is named "MIC6".','io.in.LCL.6.name','Rename LCL 6 to MIC6.'),
 ('A06','Low','Name mismatches: Ch 2 "LEAD MIC" vs port LCL 2 "LEAD MIC2"; Ch 3-5 "MIC3/4/5" vs ports "MIC 3/4/5".','ch.2.name; io.in.LCL.2-5','Align naming.'),
 ('A07','Med','USB multitrack (USB 1-48) omits Ch 8 MIC8 and LCL 21/22 VIDEO; Ch 7 uses two tracks (L/R split of a mono channel).','out.USB 1-48; USR 17-24','Decide whether MIC8 and VIDEO need recording; reclaim one Ch7 track.'),
 ('A08','Low','USB 43-48 send raw unnamed ports B7, B8, B19, B20 and C1/C2 (C-ABLE1-2); A7/A8 also direct.','out.USB 41-48','Confirm these are intended sources.'),
 ('A09','Info','Ch 9-16 have alternate sources A1-A8 configured, but the global alt switch is OFF (main source B9-B17 is live).','ch.9-16.in.conn.alt*; io.altsw=false','Know this for failover.'),
 ('A10','Info','SD/card (CRD), MOD, SC, REC and AES outputs are all OFF though the WING-LIVE card is set for 32 tracks.','out.CRD/MOD/SC/REC/AES; cards.wlive','Patch CRD outs if SD recording is planned.'),
 ('A11','Info','Talkback Ch 29-32 (B21-24) are off the mains and go to IEM1-4 (-10 dB) plus Matrix 8 TB P16 only.','ch.29-32','OK as configured.'),
 ('A12','Info','Ch 33-37 (A1-A5) and Aux 1-8 (C1-C15) are unnamed with faders at -inf; Ch 38 DJ, 39 VIDEO, 40 OSC at -inf.','ch.33-40; aux.1-8','Name or leave as spares.'),
 ('A13','Info','Output index decoding (BUS/MAIN n -> bus ceil(n/2), odd=L even=R) is inferred from the patch pattern, not a vendor document.','Snapshot Info sheet','Spot-check one output on the console.'),
]
ws = wb.create_sheet('Audit Flags', 0)
ws.append(['ID','Severity','Finding','Evidence (snapshot path)','Suggested action'])
for c in ws[1]: c.font = H; c.fill = F
for f in flags: ws.append(f)
for col, w in zip('ABCDE', (6,18,90,40,55)): ws.column_dimensions[col].width = w
log = wb.create_sheet('Master Log Row')
log.append(['Recorded date (UTC)','Project','Update','Evidence','Next action'])
log.append(['2026-11-18','DPSC Live Sound — WING scene DPSC_2026_DEFAULT_1A',
 'Input/output routing extracted and audited from DPSC_2026_DEFAULT_1A.snap (Wing-Edit 3.3.3, created 2026-09-14 12:26:55): 40 ch + 8 aux sources, 162 active output patches, 56 user signals; 13 audit flags (3 High: MTX5 Ableton P16 unrouted, HOUSE main at -inf, IEM5-8 patched but unfed).',
 'SHA-256 32b8af9d34c4bd4869e09f7d42dc173a0148c4acc0a9f77870b431a2c2266482; workbook DPSC_2026_DEFAULT_1A_routing; git branch claude/scene-input-output-routing-uoshsw (dpsouthcack/oneone)',
 'DP to confirm/resolve flags A01-A03 and A05; spot-check output index decode (A13) on console.'])
log.append(['2026-11-18','DPSC Live Sound — WING scene DPSC_2026_DEFAULT_1A',
 'Revision DPSC_2026_DEFAULT_1A_rev1.snap created: (1) A01 fixed — User Signal 13 (P16 slot 13, outputs A45/B45/C45) repointed from Aux 1 PRE to Matrix 5 ABLETON P16 POST L+R; Aux 1 alone no longer has its own P16 slot (it is still inside Matrix 5). (2) A05 fixed — input LCL 6 renamed MIC8 -> MIC6. Original file untouched.',
 'rev1 SHA-256 69e54e909efa86ef52177888cc77b61fa6f37f0561d878f041330139fcdbc0f6; JSON key diff vs original = exactly 4 keys (io.in.LCL.6.name, io.in.USR.13.user.grp/in/tap); CRLF and 41408 lines preserved',
 'Load rev1 in Wing-Edit / console; confirm P16 channel 13 hears Ableton, then relabel P16 ch13 on the personal mixers. Open: A02, A03.'])
ch = wb.create_sheet('Change Log')
ch.append(['Date (UTC)','File','JSON path','Before','After','Reason'])
for r in [('2026-11-18','DPSC_2026_DEFAULT_1A_rev1.snap','io.in.LCL.6.name','MIC8','MIC6','A05 duplicate label'),
          ('2026-11-18','DPSC_2026_DEFAULT_1A_rev1.snap','io.in.USR.13.user.grp','AUX','MTX','A01 route Matrix 5 to P16 slot 13'),
          ('2026-11-18','DPSC_2026_DEFAULT_1A_rev1.snap','io.in.USR.13.user.in','1','5','A01'),
          ('2026-11-18','DPSC_2026_DEFAULT_1A_rev1.snap','io.in.USR.13.user.tap','PRE','POST','A01 (matches other matrix P16 slots)')]: ch.append(r)
for col, w in zip('ABCDEF', (12,32,26,8,8,40)): ch.column_dimensions[col].width = w
for col, w in zip('ABCDE', (14,40,90,60,50)): log.column_dimensions[col].width = w
wb.save(p); print('ok', wb.sheetnames)
