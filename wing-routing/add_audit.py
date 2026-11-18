import sys, openpyxl
from openpyxl.styles import Font, PatternFill
p = sys.argv[1]; wb = openpyxl.load_workbook(p)
H = Font(bold=True, color='FFFFFF'); F = PatternFill('solid', fgColor='C00000')
flags = [
 ('A01','High — RESOLVED rev1','[RESOLVED 2026-11-18 in DPSC_2026_DEFAULT_1A_rev1: User 13 (P16 slot 13 on A/B/C 45) changed from Aux 1 PRE to Matrix 5 POST L+R] Matrix 5 "ABLETON P16" is fed (Aux 1-8 send to MX5 at 0 dB) but no User Signal or output carries Matrix 5. USR 1-16 cover MTX 1,2,3,4,6,7,8 only.','io.in.USR 1-16; aux.*.send.MX5','Assign a user signal / P16 slot to Matrix 5 if Ableton is wanted on personal mixers.'),
 ('A02','High — RESOLVED rev2','[RESOLVED 2026-11-18 in rev2: main.1.fdr -144 -> 0 dB, matching Mains 2-4] Main 1 HOUSE fader is at -inf (-144 dB) in this scene, while Mains 2-4 are at 0 dB.','main.1.fdr = -144','Confirm intended (safe default) before show.'),
 ('A03','High — RESOLVED rev2','[RESOLVED 2026-11-18 in rev2: all 40 ch + 8 aux now send to Buses 9-12 at -10 dB PRE, copied from their Bus 5-8 sends] IEM5-IEM8 (Buses 9-12) are patched to A/B/C outputs but no channel or aux sends to them.','ch/aux send 9-12 all off; out A5-8, B5-8, C5-8, C17-24','Build IEM5-8 mixes or unpatch.'),
 ('A04','Med — RESOLVED rev5','[RESOLVED 2026-11-18 in rev5: 352 sends raised -inf -> -10 dB (44 strips x Bus 1-4 PRE + Bus 13-16 POST); TB ch 29-32 stay off] Stage Mon 1-4 (Buses 1-4) and FX buses 13-16 have sends switched ON but at -inf on every channel; only IEM1-4 (Buses 5-8) carry signal (-10 dB PRE).','ch.*.send 1-4,13-16 lvl -144','Expected for a template; note no FX returns or wedges will sound until raised.'),
 ('A05','Med — RESOLVED rev1','[RESOLVED 2026-11-18 in rev1: LCL 6 renamed MIC8 -> MIC6] Input port LCL 6 is labelled "MIC8" (duplicate of LCL 8 "MIC8"); channel 6 is named "MIC6".','io.in.LCL.6.name','Rename LCL 6 to MIC6.'),
 ('A06','Low','Name mismatches: Ch 2 "LEAD MIC" vs port LCL 2 "LEAD MIC2"; Ch 3-5 "MIC3/4/5" vs ports "MIC 3/4/5".','ch.2.name; io.in.LCL.2-5','Align naming.'),
 ('A07','Med — RESOLVED rev3','[RESOLVED 2026-11-18 in rev3: USB 8 = User 24 now Ch 8 MIC8 PRE L+R (was Ch 7 R duplicate); USB 45/46 now LCL 21/22 VIDEO L/R (were blank B19/B20)] USB multitrack (USB 1-48) omits Ch 8 MIC8 and LCL 21/22 VIDEO; Ch 7 uses two tracks (L/R split of a mono channel).','out.USB 1-48; USR 17-24','Decide whether MIC8 and VIDEO need recording; reclaim one Ch7 track.'),
 ('A08','Low','USB 41-44 and 47-48 send raw ports A7, A8, B7, B8 (unnamed) and C1/C2 (C-ABLE1-2). (B19/B20 removed from USB 45/46 in rev3.)','out.USB 41-48','Confirm these are intended sources.'),
 ('A09','Info','Ch 9-16 have alternate sources A1-A8 configured, but the global alt switch is OFF (main source B9-B17 is live).','ch.9-16.in.conn.alt*; io.altsw=false','Know this for failover.'),
 ('A10','Info','SD/card (CRD), MOD, SC, REC and AES outputs are all OFF though the WING-LIVE card is set for 32 tracks.','out.CRD/MOD/SC/REC/AES; cards.wlive','Patch CRD outs if SD recording is planned.'),
 ('A11','Info','Talkback Ch 29-32 (B21-24) are off the mains and go to IEM1-4 (-10 dB) plus Matrix 8 TB P16 only.','ch.29-32','OK as configured.'),
 ('A12','Info','Ch 33-37 (A1-A5) and Aux 1-8 (C1-C15) are unnamed with faders at -inf; Ch 38 DJ, 39 VIDEO, 40 OSC at -inf.','ch.33-40; aux.1-8','Name or leave as spares.'),
 ('A14','Med — RESOLVED rev4','[RESOLVED 2026-11-18 in rev4: Bus 5-12 IEM1-IEM8 faders -144 -> 0 dB, unmuted] IEM bus masters Buses 5-12 (IEM1-IEM8) are all at -inf (-144 dB). Sends are built, but no IEM will be heard until its bus fader is raised.','bus.5-12.fdr = -144','Raise each IEM master at soundcheck (left down on purpose for ear safety).'),
 ('A15','Med','Stage Mon 1-4 master faders (Buses 1-4) are at -inf (-144 dB). Wedge sends are now at -10 dB PRE, but no wedge will be heard until these masters are raised. (FX buses 13-16 masters are already 0 dB and feed Main 1 HOUSE, so FX returns are now live.)','bus.1-4.fdr = -144','Raise Stage Mon 1-4 masters (DP decision; same as IEM masters in rev4).'),
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
log.append(['2026-11-18','DPSC Live Sound — WING scene DPSC_2026_DEFAULT_1A',
 'Revision DPSC_2026_DEFAULT_1A_rev2.snap (built on rev1): (1) A02 fixed — Main 1 HOUSE fader -inf -> 0 dB. (2) A03 fixed — IEM5-8 (Buses 9-12) mixes built: Ch 1-40 and Aux 1-8 send at -10 dB PRE, mirroring IEM1-4 (Bus 9<-5, 10<-6, 11<-7, 12<-8; 192 sends). New flag A14: all IEM bus masters (Bus 5-12) still at -inf.',
 'rev2 SHA-256 25d4b5f397929ac40848e1efd37aff28145e0784bd1eccc48aa36f0596501648; JSON key diff vs rev1 = 769 values (main.1.fdr + 192 sends x on/lvl/mode/plink); same key set, CRLF and 41408 lines preserved; generator make_rev2.py',
 'Load rev2; raise IEM masters and tailor IEM5-8 mixes at soundcheck; confirm HOUSE level before opening PA.'])
import json as _j
_r1 = _j.load(open('DPSC_2026_DEFAULT_1A_rev1.snap'))['ae_data']
def _b(g,n,b):
    v=_r1[g][str(n)]['send'][str(b)]; return f"{'on' if v['on'] else 'off'}/{v['lvl']:g}/{v['mode']}/plink{v['plink']}"
log.append(['2026-11-18','DPSC Live Sound — WING house rules',
 'DP standing rule recorded: never use GRP send taps — always PRE or POST; IEM sends always PRE. Rule Checks sheet added to the routing audit (auto-checks every ch/aux send). rev2 checked: 0 GRP sends, all 384 IEM1-8 sends PRE = PASS. Original and rev1 had 96 GRP (old IEM5-8 sends; replaced in rev2). No scene change needed.',
 'grep count "GRP": original 96, rev1 96, rev2 0; Rule Checks sheet R1/R2 PASS',
 'Add to Operating Notes in Master as a standing WING rule; apply on every future scene edit.'])
log.append(['2026-11-18','DPSC Live Sound — WING scene DPSC_2026_DEFAULT_1A',
 'Revision DPSC_2026_DEFAULT_1A_rev3.snap (built on rev2): A07 fixed — USB recording now includes MIC8 and VIDEO. USB 8: User 24 changed Ch 7 PRE R (duplicate of mono MIC7) -> Ch 8 MIC8 PRE L+R. USB 45/46: B19/B20 (blank, unused) -> LCL 21/22 VIDEO L/R raw, same method as DJ. Ch 7 MIC7 still recorded on USB 7. B19/B20 no longer recorded.',
 'rev3 SHA-256 5dad4873fa2ca08f489eeeba2e57721fdff5c964534f7e155e4ee1ca79c287a2; diff vs rev2 = 6 values (io.in.USR.24.user.in/lr, io.out.USB.45/46 grp/in); B19/B20 verified unused by any strip, alt source or user signal; 0 GRP; Rule Checks PASS; CRLF and 41408 lines preserved; generator make_rev3.py',
 'Load rev3; arm USB 8 and 45/46 in DAW and rename tracks (MIC8, VIDEO L, VIDEO R).'])
log.append(['2026-11-18','DPSC Live Sound — WING house rules',
 'DP standing rule recorded: recording does not need to include talkback mics. rev3 checked: TB Ch 29-32 (B21-24) and Matrix 8 TB P16 are on none of USB 1-48; CRD and REC outputs all OFF. Already compliant — no scene change. Rule R3 added to Rule Checks (auto-check of USB/CRD/REC outputs, resolving user signals).',
 'Rule Checks R1/R2/R3 PASS on rev3 (SHA-256 5dad4873fa2ca08f489eeeba2e57721fdff5c964534f7e155e4ee1ca79c287a2)',
 'Add to Master Operating Notes as a standing WING rule alongside never-GRP / IEM-PRE.'])
log.append(['2026-11-18','DPSC Live Sound — WING scene DPSC_2026_DEFAULT_1A',
 'Revision DPSC_2026_DEFAULT_1A_rev4.snap (built on rev3): A14 fixed — IEM1-IEM8 master faders (Buses 5-12) raised from -inf to 0 dB at DP request. With every ch/aux sending -10 dB PRE, all eight IEM mixes are now live on scene load.',
 'rev4 SHA-256 c8653c86d48d0cbbd6c52ac9ce09e820a1fbd3a750d25df6f1757c89b2d8cd33; diff vs rev3 = 8 values (bus.5-12.fdr); same key set; 0 GRP; Rule Checks R1/R2/R3 PASS; CRLF and 41408 lines preserved; generator make_rev4.py',
 'Ear safety: keep IEM transmitters/packs down when loading rev4; set levels at soundcheck.'])
log.append(['2026-11-18','DPSC Live Sound — WING scene DPSC_2026_DEFAULT_1A',
 'Revision DPSC_2026_DEFAULT_1A_rev5.snap (built on rev4): A04 fixed — stage monitor and FX sends brought up. Every send already switched ON to Stage Mon 1-4 (Bus 1-4, PRE) and PLATE/HALL/SH DELAY/LG DELAY (Bus 13-16, POST) raised from -inf to -10 dB, matching IEM send level: Ch 1-28, 33-40 and Aux 1-8 (44 strips, 352 sends). Taps unchanged. Talkback Ch 29-32 sends remain OFF. New flag A15: Stage Mon 1-4 masters still -inf; FX masters at 0 dB so FX now reaches HOUSE.',
 'rev5 SHA-256 e6e30bce79dd887ed2e79845f97a52896408bee81f4cfec891e815ea1e71520b; diff vs rev4 = 352 values, all send lvl -144 -> -10 on buses 1-4/13-16; same key set; 0 GRP; Rule Checks R1/R2/R3 PASS; CRLF and 41408 lines preserved; generator make_rev5.py',
 'DP to decide Stage Mon 1-4 master level (A15); trim FX send levels per source at soundcheck.'])
ch = wb.create_sheet('Change Log')
ch.append(['Date (UTC)','File','JSON path','Before','After','Reason'])
for r in [('2026-11-18','DPSC_2026_DEFAULT_1A_rev1.snap','io.in.LCL.6.name','MIC8','MIC6','A05 duplicate label'),
          ('2026-11-18','DPSC_2026_DEFAULT_1A_rev1.snap','io.in.USR.13.user.grp','AUX','MTX','A01 route Matrix 5 to P16 slot 13'),
          ('2026-11-18','DPSC_2026_DEFAULT_1A_rev1.snap','io.in.USR.13.user.in','1','5','A01'),
          ('2026-11-18','DPSC_2026_DEFAULT_1A_rev1.snap','io.in.USR.13.user.tap','PRE','POST','A01 (matches other matrix P16 slots)'),
          ('2026-11-18','DPSC_2026_DEFAULT_1A_rev2.snap','main.1.fdr','-144','0','A02 HOUSE to unity'),
          ('2026-11-18','DPSC_2026_DEFAULT_1A_rev3.snap','io.in.USR.24.user','CH 7 PRE R','CH 8 PRE L+R','A07 USB 8 records MIC8'),
          ('2026-11-18','DPSC_2026_DEFAULT_1A_rev3.snap','io.out.USB.45','B 19','LCL 21','A07 USB 45 records VIDEO L'),
          ('2026-11-18','DPSC_2026_DEFAULT_1A_rev3.snap','io.out.USB.46','B 20','LCL 22','A07 USB 46 records VIDEO R')] + [
          ('2026-11-18','DPSC_2026_DEFAULT_1A_rev4.snap',f'bus.{b}.fdr','-144','0',f'A14 IEM{b-4} master to 0 dB') for b in range(5,13)] + [
          ('2026-11-18','DPSC_2026_DEFAULT_1A_rev5.snap',f'{g}.{n}.send.{b}.lvl','-144','-10',f'A04 {"Stage Mon "+str(b) if b<5 else "FX bus "+str(b)} send')
          for g,r in (('ch',[*range(1,29),*range(33,41)]),('aux',range(1,9))) for n in r for b in (1,2,3,4,13,14,15,16)] + [
          ('2026-11-18','DPSC_2026_DEFAULT_1A_rev2.snap',f'{g}.{n}.send.{b}',_b(g,n,b),'on/-10/PRE/plink0',f'A03 IEM{b-4} mirrors Bus {b-4} send')
          for g,r in (('ch',range(1,41)),('aux',range(1,9))) for n in r for b in (9,10,11,12)]: ch.append(r)
for col, w in zip('ABCDEF', (12,32,26,8,8,40)): ch.column_dimensions[col].width = w
for col, w in zip('ABCDE', (14,40,90,60,50)): log.column_dimensions[col].width = w
wb.save(p); print('ok', wb.sheetnames)
