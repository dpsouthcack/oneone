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
 ('A06','Low — RESOLVED rev7','[RESOLVED 2026-11-18 in rev7: Ch 2 -> LEAD MIC2; LCL 3-5 -> MIC3/MIC4/MIC5; Ch 1-8 names now equal their input port names] Name mismatches: Ch 2 "LEAD MIC" vs port LCL 2 "LEAD MIC2"; Ch 3-5 "MIC3/4/5" vs ports "MIC 3/4/5".','ch.2.name; io.in.LCL.2-5','Align naming.'),
 ('A07','Med — RESOLVED rev3','[RESOLVED 2026-11-18 in rev3: USB 8 = User 24 now Ch 8 MIC8 PRE L+R (was Ch 7 R duplicate); USB 45/46 now LCL 21/22 VIDEO L/R (were blank B19/B20)] USB multitrack (USB 1-48) omits Ch 8 MIC8 and LCL 21/22 VIDEO; Ch 7 uses two tracks (L/R split of a mono channel).','out.USB 1-48; USR 17-24','Decide whether MIC8 and VIDEO need recording; reclaim one Ch7 track.'),
 ('A08','Low — CLOSED (DP confirmed intended)','[CLOSED 2026-11-18: DP confirmed these raw USB sources are intended; leave as-is, no scene change] USB 41-44 and 47-48 send raw ports A7, A8, B7, B8 (unnamed) and C1/C2 (C-ABLE1-2). (B19/B20 removed from USB 45/46 in rev3.)','out.USB 41-48','Confirm these are intended sources.'),
 ('A09','Info','Ch 9-16 have alternate sources A1-A8 configured, but the global alt switch is OFF (main source B9-B17 is live).','ch.9-16.in.conn.alt*; io.altsw=false','Know this for failover.'),
 ('A10','Info','SD/card (CRD), MOD, SC, REC and AES outputs are all OFF though the WING-LIVE card is set for 32 tracks.','out.CRD/MOD/SC/REC/AES; cards.wlive','Patch CRD outs if SD recording is planned.'),
 ('A11','Info','Talkback Ch 29-32 (B21-24) are off the mains and go to IEM1-4 (-10 dB) plus Matrix 8 TB P16 only.','ch.29-32','OK as configured.'),
 ('A12','Info — RESOLVED rev8','[RESOLVED 2026-11-18 in rev8: Ch 33-37 named KICK/SNARE/HIHAT/T1/T2 ALT; Aux 1-6 named from DCA tags TRAX, TRAX-DRUMS, TRAX-BASS, TRAX-KEYS, TRAX-GUITARS, TRAX-VOX; Aux 7-8 TRAX 13-14 / TRAX 15-16] Ch 33-37 (A1-A5) and Aux 1-8 (C1-C15) were unnamed with faders at -inf; Ch 38 DJ, 39 VIDEO, 40 OSC at -inf.','ch.33-40; aux.1-8','Name or leave as spares.'),
 ('A14','Med — RESOLVED rev4','[RESOLVED 2026-11-18 in rev4: Bus 5-12 IEM1-IEM8 faders -144 -> 0 dB, unmuted] IEM bus masters Buses 5-12 (IEM1-IEM8) are all at -inf (-144 dB). Sends are built, but no IEM will be heard until its bus fader is raised.','bus.5-12.fdr = -144','Raise each IEM master at soundcheck (left down on purpose for ear safety).'),
 ('A15','Med — RESOLVED rev6','[RESOLVED 2026-11-18 in rev6: Bus 1-4 STAGE MON1-4 faders -144 -> 0 dB, unmuted] Stage Mon 1-4 master faders (Buses 1-4) are at -inf (-144 dB). Wedge sends are now at -10 dB PRE, but no wedge will be heard until these masters are raised. (FX buses 13-16 masters are already 0 dB and feed Main 1 HOUSE, so FX returns are now live.)','bus.1-4.fdr = -144','Raise Stage Mon 1-4 masters (DP decision; same as IEM masters in rev4).'),
 ('A16','High — RESOLVED rev10/rev11','[RESOLVED 2026-11-18: rev10 removed CLICK/CUES from HOUSE, SUBS, DELAY, STAGE MON1-4 and FX buses 13-16; rev11 removed them from STREAM and from Matrix 5 ABLETON P16, and gave them their own P16 channel: Matrix 4 renamed CLK+CUE P16 (was empty XTRA P16) on P16 slot 11 (User 11, outputs A43/B43/C43). Now on IEM1-8 PRE and CLK+CUE P16 only] CLICK (Aux 7) and CUES (Aux 8) are routed like program audio: assigned to HOUSE 0 dB, SUBS 0 dB, DELAY 0 dB, STREAM -10 dB (live once their -inf faders are raised), sent POST -10 dB to PLATE/HALL/SH DELAY/LG DELAY, and sent PRE -10 dB to STAGE MON1-4 and to Matrix 5 ABLETON P16 - PRE sends are live now regardless of the fader, so click/cues reach the wedges. IEM1-8 PRE sends (-10 dB) are normally wanted.','aux.7-8.main 1-4; aux.7-8.send 1-4, 13-16, MX5','DP decision: remove CLICK/CUES from mains, FX and wedges (keep IEMs); decide whether they stay in ABLETON P16 or get their own P16 slots.'),
 ('A13','Info — CLOSED (DP verified on console)','[CLOSED 2026-11-18: DP verified on the console that the output decode is correct] Output index decoding (BUS/MAIN n -> bus ceil(n/2), odd=L even=R) is inferred from the patch pattern, not a vendor document.','Snapshot Info sheet','Spot-check one output on the console.'),
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
log.append(['2026-11-18','DPSC Live Sound — WING scene DPSC_2026_DEFAULT_1A',
 'Revision DPSC_2026_DEFAULT_1A_rev6.snap (built on rev5): A15 fixed — STAGE MON1-4 master faders (Buses 1-4) raised from -inf to 0 dB at DP request. All 16 buses and 4 mains now at 0 dB, none muted; wedges live on scene load (GEQ inserts FX9-12 remain in place).',
 'rev6 SHA-256 7a460382c00443dc6574bfb0d8d52ddb8880b936f6c91604e79e380c3b2f75f1; diff vs rev5 = 4 values (bus.1-4.fdr); same key set; 0 GRP; Rule Checks R1/R2/R3 PASS; CRLF and 41408 lines preserved; generator make_rev6.py',
 'Keep wedge amps down when loading rev6; ring out wedges at soundcheck. Open: A06, A08, A13.'])
log.append(['2026-11-18','DPSC Live Sound — WING scene DPSC_2026_DEFAULT_1A',
 'Revision DPSC_2026_DEFAULT_1A_rev7.snap (built on rev6): A06 fixed — naming mismatches. Ch 2 renamed LEAD MIC -> LEAD MIC2 (matches port LCL 2 and Ch 1 LEAD MIC1). Ports LCL 3/4/5 renamed MIC 3/4/5 -> MIC3/MIC4/MIC5 (match Ch 3-5 and MIC6-8 no-space style). Full scan: Ch 1-8 strip names now equal port names. Remaining strip/port differences are blank spare names only (Ch 34-37, Ch 40 OSC, Aux 1-8; flag A12), left unchanged.',
 'rev7 SHA-256 403830931baab4ab0d97c1dd7cf34dd28e620c54377d8422d05b61c1dddeb4f2; diff vs rev6 = 4 values (ch.2.name, io.in.LCL.3/4/5.name); 0 GRP; Rule Checks R1/R2/R3 PASS; CRLF and 41408 lines preserved; generator make_rev7.py',
 'Open: A08 (confirm raw USB sources), A13 (spot-check output decode on console).'])
log.append(['2026-11-18','DPSC Live Sound — WING scene DPSC_2026_DEFAULT_1A',
 'A08 closed: DP confirmed raw USB sources are intended — USB 41-44 = A7, A8, B7, B8; USB 47-48 = C1/C2 (C-ABLE1-2). Leave as-is. No scene change; rev7 remains current.',
 'DP instruction in session 2026-11-18; rev7 SHA-256 403830931baab4ab0d97c1dd7cf34dd28e620c54377d8422d05b61c1dddeb4f2 unchanged',
 'Only open item: A13 (spot-check output index decode on console).'])
log.append(['2026-11-18','DPSC Live Sound — WING scene DPSC_2026_DEFAULT_1A',
 'A13 closed: DP verified on the console that the output index decode is correct (BUS/MAIN n -> bus ceil(n/2), odd=L, even=R). The Output Patch decode is confirmed, not inferred. All actionable audit flags are now resolved or closed; A09-A12 remain informational. rev7 is the current scene.',
 'DP console verification reported in session 2026-11-18; rev7 SHA-256 403830931baab4ab0d97c1dd7cf34dd28e620c54377d8422d05b61c1dddeb4f2 unchanged',
 'None open. Paste Update Log rows into Master; add house rules (never GRP, IEM PRE, no TB in recording) to Operating Notes.'])
log.append(['2026-11-18','DPSC Live Sound — WING scene DPSC_2026_DEFAULT_1A',
 'Revision DPSC_2026_DEFAULT_1A_rev8.snap (built on rev7): spare strips named. Ch 33-37 (inputs A1-A5 = alt/backup sources of Ch 9-13) -> KICK ALT, SNARE ALT, HIHAT ALT, T1 ALT, T2 ALT. Aux 1-6 (Ableton C-ABLE pairs; already in DCAs 8-13) -> TRAX, TRAX-DRUMS, TRAX-BASS, TRAX-KEYS, TRAX-GUITARS, TRAX-VOX (DCA names). Aux 7-8 (no DCA; C13-16) -> TRAX 13-14, TRAX 15-16. Port names, DCA tags and colours unchanged.',
 'rev8 SHA-256 0e4d3746c6f8791d39d0fb9ec5c402cc97a100eab185d2a9da4dc2160b0ccf85; diff vs rev7 = 13 name values (ch.33-37.name, aux.1-8.name); names <= 12 chars; 0 GRP; Rule Checks R1/R2/R3 PASS; CRLF and 41408 lines preserved; generator make_rev8.py',
 'DP to confirm Aux 7-8 content (no DCA evidence) and rename if needed. Remaining blank: input port A1 name, Ch 40 OSC port (oscillator).'])
log.append(['2026-11-18','DPSC Live Sound — WING scene DPSC_2026_DEFAULT_1A',
 'Revision DPSC_2026_DEFAULT_1A_rev9.snap (built on rev8): DP identified Aux 7 = CLICK, Aux 8 = CUES; renamed from TRAX 13-14 / TRAX 15-16. New flag A16 (High): CLICK/CUES routed like program audio — mains 1-4, FX sends, PRE to STAGE MON1-4 and Matrix 5 ABLETON P16. Routing NOT changed pending DP decision.',
 'rev9 SHA-256 cdd8e681492b2d6d38580d427dafb65db5b7acf21807f8947620942ac715245b; diff vs rev8 = 2 values (aux.7.name, aux.8.name); 0 GRP; Rule Checks PASS; CRLF and 41408 lines preserved; generator make_rev9.py',
 'DP to decide A16: remove CLICK/CUES from HOUSE/SUBS/DELAY/STREAM, FX and wedges; keep IEMs; P16 handling.'])
log.append(['2026-11-18','DPSC Live Sound — WING house rules + scene DPSC_2026_DEFAULT_1A',
 'DP standing rule: click and cues must never come out of the house PA or any floor monitor. Revision DPSC_2026_DEFAULT_1A_rev10.snap (built on rev9): CLICK (Aux 7) and CUES (Aux 8) unassigned from HOUSE, SUBS, DELAY mains; sends switched OFF to STAGE MON1-4 and to PLATE/HALL/SH DELAY/LG DELAY (FX buses feed HOUSE, so would leak click into PA). Kept: IEM1-8 PRE -10 dB, Matrix 5 ABLETON P16 PRE 0 dB (P16 personal mixers), STREAM main -10 dB (not house; pending DP). Rule R4 added to Rule Checks.',
 'rev10 SHA-256 af731c4adacdf92c3d2a1bebfd5c6092a10c6b758848003dfaf887656199c7a0; diff vs rev9 = 22 values, all on true -> false (aux.7/8 main 1-3, send 1-4, 13-16); same key set; 0 GRP; Rule Checks R1-R4 PASS on rev10, R4 FAILs on rev9 (22); CRLF and 41408 lines preserved; generator make_rev10.py',
 'DP to decide whether CLICK/CUES stay on STREAM. Add R4 to Master Operating Notes as a standing WING rule.'])
log.append(['2026-11-18','DPSC Live Sound — WING house rules + scene DPSC_2026_DEFAULT_1A',
 'DP rule extended: click and cues must not go to STREAM either (i.e. no main at all, no floor monitors), and should have their own P16 channel. Revision DPSC_2026_DEFAULT_1A_rev11.snap (built on rev10): CLICK/CUES unassigned from Main 4 STREAM; removed from Matrix 5 ABLETON P16 (slot 13 now TRAX stems only); Matrix 4 XTRA P16 (verified no inputs) renamed CLK+CUE P16 and fed by CLICK and CUES at 0 dB PRE, reaching P16 slot 11 via User 11 (MTX4 POST L+R) on outputs A43/B43/C43. CLICK/CUES now reach IEM1-8 (-10 dB PRE) and CLK+CUE P16 only. Rule R4 widened to all mains incl. STREAM.',
 'rev11 SHA-256 15158347297e628058db36f63575f0ee7608ead9a63afa8aa2f2f5cd1e91e098; diff vs rev10 = 9 values (aux.7/8 main.4.on, send.MX5.on, send.MX4.on/lvl; mtx.4.name); MX4 had zero sends before (asserted in make_rev11.py); same key set; 0 GRP; Rule Checks R1-R4 PASS on rev11, R4 FAILs on rev10 (STREAM x2); CRLF and 41408 lines preserved',
 'On P16s: label channel 11 CLK+CUE (was XTRA). Click and cues share one P16 channel; separate channels would need another P16 slot freed. Update Master Operating Notes R4 wording (no mains incl. STREAM).'])
log.append(['2026-11-18','DPSC Live Sound — WING scene DPSC_2026_DEFAULT_1A',
 'DP confirmed: CLICK and CUES sharing one P16 channel (CLK+CUE P16, Matrix 4, P16 slot 11) is fine — keep it. No scene change; rev11 remains current.',
 'DP instruction in session 2026-11-18; rev11 SHA-256 15158347297e628058db36f63575f0ee7608ead9a63afa8aa2f2f5cd1e91e098 unchanged',
 'None open. Paste Update Log rows into Master; add house rules R1-R4 to Operating Notes; relabel P16 ch 11 CLK+CUE.'])
log.append(['2026-11-18','DPSC Live Sound — WING scene DPSC_2026_DEFAULT_1A',
 'Revision DPSC_2026_DEFAULT_1A_rev12.snap (built on rev11): DP rule — MIC8 should not have its own P16 channel. P16 slot 12 (outputs A44/B44/C44, was User 12 = Ch 8 MIC8 PRE) set OFF; slot 12 now empty per DP. MIC8 added to Matrix 6 MICS P16 at 0 dB PRE (same as MIC3-6), so MICS P16 = MIC3, MIC4, MIC5, MIC6, MIC8. User 12 definition left in place but unused (no OFF user-signal example in file; outputs OFF is the proven format).',
 'rev12 SHA-256 41002da4ebcce6fffafa3a37c3ccec2fa3e09e2a0c9b667cb48a5f5005ffe420; diff vs rev11 = 8 values (io.out.A/B/C.44 grp/in, ch.8.send.MX6 on/lvl); same key set; 0 GRP; Rule Checks R1-R4 PASS; CRLF and 41408 lines preserved; generator make_rev12.py',
 'On P16s: clear/relabel channel 12 (was MIC8). Note MIC7 is in no P16 mix (unchanged).'])
log.append(['2026-11-18','DPSC Live Sound — WING scene DPSC_2026_DEFAULT_1A',
 'P16 routing review (DP thought all 16 slots were represented / recalled a bus feeding one). Original vs rev12: no bus or main ever sent to any matrix; no matrix direct inputs; matrices reach P16 only via user signals. Original anomalies: slot 11 Matrix 4 XTRA P16 had NO inputs (empty slot all along; now CLK+CUE P16), slot 13 was Aux 1 only while the ABLETON P16 matrix (Aux 1-8) was unrouted (fixed rev1). rev12: slot 12 EMPTY (MIC8 moved to MICS P16). Strips on no P16 slot in rev12: MIC7, B5, B6, B31, B32, KICK/SNARE/HIHAT/T1/T2 ALT, DJ, VIDEO, OSC 1. P16 Map tab added to the workbook.',
 'p16_view.py comparison of original (SHA-256 32b8af9d...) and rev12 (41002da4...); outputs A/B/C 33-48 identical across A, B, C in both',
 'DP to decide: what (if anything) goes on slot 12; whether MIC7 / DJ / VIDEO should reach the P16s.'])
log.append(['2026-11-18','DPSC Live Sound — WING scene DPSC_2026_DEFAULT_1A',
 'Revision DPSC_2026_DEFAULT_1A_rev13.snap (built on rev12): DP — MIC7 also goes in MICS P16. Ch 7 MIC7 send to Matrix 6 MICS P16 set on at 0 dB PRE (same as MIC3-6, MIC8). MICS P16 (P16 slot 14) = MIC3, MIC4, MIC5, MIC6, MIC7, MIC8.',
 'rev13 SHA-256 e2d39306b0812850b7b5a8ab7b6685264359a0b2037b7bef5167bb7b7ef886ac; diff vs rev12 = 2 values (ch.7.send.MX6 on/lvl); 0 GRP; Rule Checks R1-R4 PASS; CRLF and 41408 lines preserved; generator make_rev13.py',
 'Slot 12 remains empty — DP to decide (DJ, VIDEO, or a bus).'])
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
          ('2026-11-18','DPSC_2026_DEFAULT_1A_rev6.snap',f'bus.{b}.fdr','-144','0',f'A15 STAGE MON{b} master to 0 dB') for b in range(1,5)] + [
          ('2026-11-18','DPSC_2026_DEFAULT_1A_rev7.snap','ch.2.name','LEAD MIC','LEAD MIC2','A06 match port LCL 2'),
          ('2026-11-18','DPSC_2026_DEFAULT_1A_rev7.snap','io.in.LCL.3.name','MIC 3','MIC3','A06 match Ch 3'),
          ('2026-11-18','DPSC_2026_DEFAULT_1A_rev7.snap','io.in.LCL.4.name','MIC 4','MIC4','A06 match Ch 4'),
          ('2026-11-18','DPSC_2026_DEFAULT_1A_rev7.snap','io.in.LCL.5.name','MIC 5','MIC5','A06 match Ch 5')] + [
          ('2026-11-18','DPSC_2026_DEFAULT_1A_rev8.snap',f'ch.{n}.name','(blank)',f'{p} ALT',f'A12 input A{n-32} = alt source of Ch {n-24}') for n,p in zip(range(33,38),['KICK','SNARE','HIHAT','T1','T2'])] + [
          ('2026-11-18','DPSC_2026_DEFAULT_1A_rev8.snap',f'aux.{n}.name','(blank)',nm,why) for n,nm,why in [
           (1,'TRAX','A12 DCA 8 tag #D8'),(2,'TRAX-DRUMS','A12 DCA 9 tag #D9'),(3,'TRAX-BASS','A12 DCA 10 tag #D10'),(4,'TRAX-KEYS','A12 DCA 11 tag #D11'),
           (5,'TRAX-GUITARS','A12 DCA 12 tag #D12'),(6,'TRAX-VOX','A12 DCA 13 tag #D13'),(7,'TRAX 13-14','A12 no DCA; port C-ABLE13-14'),(8,'TRAX 15-16','A12 no DCA; port C-ABLE15-16')]] + [
          ('2026-11-18','DPSC_2026_DEFAULT_1A_rev9.snap','aux.7.name','TRAX 13-14','CLICK','DP identified Aux 7 as click'),
          ('2026-11-18','DPSC_2026_DEFAULT_1A_rev9.snap','aux.8.name','TRAX 15-16','CUES','DP identified Aux 8 as cues')] + [
          ('2026-11-18','DPSC_2026_DEFAULT_1A_rev10.snap',f'aux.{n}.{path}.on','true','false',f'A16/R4 {nm} out of {dest}')
          for n,nm in ((7,'CLICK'),(8,'CUES')) for path,dest in [('main.1','HOUSE'),('main.2','SUBS'),('main.3','DELAY'),('send.1','STAGE MON1'),('send.2','STAGE MON2'),('send.3','STAGE MON3'),('send.4','STAGE MON4'),('send.13','PLATE (feeds HOUSE)'),('send.14','HALL (feeds HOUSE)'),('send.15','SH DELAY (feeds HOUSE)'),('send.16','LG DELAY (feeds HOUSE)')]] + [
          ('2026-11-18','DPSC_2026_DEFAULT_1A_rev11.snap',f'aux.{n}.{path}',b,af,why) for n,nm in ((7,'CLICK'),(8,'CUES')) for path,b,af,why in [
            ('main.4.on','true','false',f'R4 {nm} out of STREAM'),('send.MX5.on','true','false',f'{nm} out of ABLETON P16'),
            ('send.MX4.on','false','true',f'{nm} into own P16 channel'),('send.MX4.lvl','-144','0',f'{nm} into own P16 channel (PRE)')]] + [
          ('2026-11-18','DPSC_2026_DEFAULT_1A_rev11.snap','mtx.4.name','XTRA P16','CLK+CUE P16','Empty matrix repurposed as click/cues P16 channel (slot 11)')] + [
          ('2026-11-18','DPSC_2026_DEFAULT_1A_rev12.snap',f'io.out.{g}.44','USR 12 (Ch 8 MIC8 PRE)','OFF','DP: MIC8 no own P16 slot; slot 12 empty') for g in 'ABC'] + [
          ('2026-11-18','DPSC_2026_DEFAULT_1A_rev12.snap','ch.8.send.MX6','off/-144/PRE','on/0/PRE','DP: MIC8 into MICS P16 (matches MIC3-6)'),
          ('2026-11-18','DPSC_2026_DEFAULT_1A_rev13.snap','ch.7.send.MX6','off/-144/PRE','on/0/PRE','DP: MIC7 into MICS P16')] + [
          ('2026-11-18','DPSC_2026_DEFAULT_1A_rev2.snap',f'{g}.{n}.send.{b}',_b(g,n,b),'on/-10/PRE/plink0',f'A03 IEM{b-4} mirrors Bus {b-4} send')
          for g,r in (('ch',range(1,41)),('aux',range(1,9))) for n in r for b in (9,10,11,12)]: ch.append(r)
for col, w in zip('ABCDEF', (12,32,26,8,8,40)): ch.column_dimensions[col].width = w
for col, w in zip('ABCDE', (14,40,90,60,50)): log.column_dimensions[col].width = w
wb.save(p); print('ok', wb.sheetnames)
