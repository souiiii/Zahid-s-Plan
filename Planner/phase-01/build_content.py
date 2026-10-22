"""Build clock-independent topic assignments from the approved resource pool."""
from pathlib import Path
from datetime import date,timedelta
import json

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
pool=json.loads((ROOT/'Resources/phase-01/pool.json').read_text())
R={r['id']:r for r in pool['resources']}
P={p['id']:p for p in pool['practice_sets']}

def res(rid,label=None,page=None):
 r=R[rid];url=r.get('path') or r['url']
 if page is not None:url+='#page='+str(page)
 return dict(label=label or r['title'],url=url,resource_id=rid)
def pack(subject,page,label):
 return dict(label=label,url=f'Resources/phase-01/{subject}-board-practice.pdf#page={page}')
def video(rid,start,end):
 return dict(resource_id=rid,url=R[rid]['url']+f'&t={start}s',start_seconds=start,end_seconds=end,
             label=f"Main lesson · {start//3600}:{start//60%60:02}:{start%60:02}–{end//3600}:{end//60%60:02}:{end%60:02}",
             locator_type='Sequential playback window; not a claimed publisher topic marker')
def task(subject,title,learn,practice,output,links,ids,minutes,clip=None):
 return dict(subject=subject,title=title,learn=learn,practice=practice,output=output,resources=links,
             pool_practice_ids=ids,target_minutes=minutes,video=clip)

math=[
 ('Continuity · limits & first piecewise checks','Read NCERT 5.2, PDF pp. 1–13. Test continuity using LHL = RHL = f(a); simplify a removable discontinuity before substituting.','Ex. 5.1 Q1, Q3 (all parts), Q6 and Q12. Show both one-sided limits at each joining point.','Four question attempts, corrections and a 3-line continuity test.',13,['M-NP01']),
 ('Continuity · matching constants','Read the worked piecewise examples and finish 5.2, PDF pp. 13–15. Distinguish the function value from its limit.','Ex. 5.1 Q17, Q24, Q26 and Q30. Then 2026 65/1/1 Q21(a), pack p. 1.','Constants/limits justified, including the two-constant matching problem.',14,['M-NP01','M-BP01']),
 ('Differentiability · chain rule','Read 5.3, PDF pp. 15–19. Recall product/quotient rules; write the inner and outer function before differentiating.','Ex. 5.2 Q1, Q2, Q5, Q6 and Q9. For Q9, compare left and right derivatives.','Five independent attempts; explain why a continuous corner may fail differentiability.',19,['M-NP02']),
 ('Implicit & inverse-trig derivatives','Read 5.3.2–5.3.3, PDF pp. 20–22. Differentiate y-terms with dy/dx, then collect them on one side.','Ex. 5.3 Q1, Q5, Q9 and Q10; 2026 65/1/1 Q21(b), pack p. 1.','Four exercises plus the board alternative, with inverse-trig domain restrictions retained.',22,['M-NP03','M-BP01']),
 ('Exponential & logarithmic derivatives','Read 5.4–5.5, PDF pp. 23–31. Separate log of a function from a function raised to a variable power.','Ex. 5.4 Q1, Q4, Q5 and Q8; Ex. 5.5 Q3 and Q4. Attempt the last two after taking logs.','Six attempts; a small rule card for exp/log/variable-power differentiation.',27,['M-NP04','M-NP05']),
 ('Log differentiation · consolidate','Finish the main lesson if needed. Read the log-differentiation worked examples, then close them.','Ex. 5.5 Q7 and Q12. Reattempt the incorrect item, if any, from yesterday’s Ex. 5.5 Q3 or Q4; otherwise rederive Q7 without looking.','All four selected Ex. 5.5 questions attempted across the two days; corrected log steps.',31,['M-NP05']),
 ('Parametric derivatives','Read 5.6, PDF pp. 32–34. Compute dy/dt and dx/dt separately, then divide. The video is optional lookup today.','Ex. 5.6 Q1, Q3, Q6 and Q8. Reattempt Q6 with both derivatives written explicitly.','Four attempts and the parametric derivative rule, including where dx/dt may vanish.',34,['M-NP06']),
 ('Second derivatives · board proof','Read 5.7, PDF pp. 35–37. For parametric second derivatives, differentiate dy/dx with respect to t and divide by dx/dt again.','Ex. 5.7 Q3, Q5, Q8, Q11 and Q14. Then 2026 65/1/1 Q34, pack p. 2.','Five exercises and one structured board proof; no skipped chain-rule factors.',36,['M-NP07','M-BP02']),
 ('Mixed NCERT & board transfer','Recall your method choices before opening a reference. Use the video only if a specific method is still unclear.','Miscellaneous Q7, Q12 and Q17; 2026 65/1/2 Q32 (pack p. 3); official SQP Q8 and Q22 (pack pp. 4–5).','Six mixed attempts; tag each error as concept, algebra, domain or presentation.',41,['M-NP08','M-BP03','M-BP04'])]

organic=[
 ('Organic base · structures & bonds','NCERT XI selected 8.2–8.4, PDF pp. 2–6: valency, expanded/condensed structures, sigma/pi bonds, sp3/sp2/sp and functional-group recognition.','Bridge check Q3, Q5 and Q6. Sketch ethanol, ethanal, ethene and ethyne with sensible valencies.','Identify the groups and count bonds without notes; do not memorise a full reaction list.',2,['O-CP01']),
 ('Organic base · naming simply','NCERT XI 8.5, PDF pp. 7–12. Pick the parent chain containing the principal functional group; number before naming substituents.','Worked Problems 8.7 and 8.8: cover their solutions first. Bridge check Q1 and Q2.','Names and structures checked against the worked solutions; record only the naming rule that caused an error.',10,['O-NP01','O-CP01']),
 ('Organic base · structures & isomers','NCERT XI 8.5.4 and selected 8.6, PDF pp. 13–16. Recognise chain/position/functional isomers and primary/secondary/tertiary carbon types.','Worked Problem 8.9; reattempt bridge check Q2 and Q4. Recognise ortho/meta/para positions using Q19.','Simple naming and isomer recognition are comfortable; no advanced stereochemistry detour.',13,['O-NP01','O-CP01']),
 ('Organic base · breaking a bond','NCERT XI 8.7.1, PDF pp. 16–17. Track the bonding electrons in heterolytic versus homolytic cleavage; recognise carbocations, carbanions and radicals.','Worked Problem 8.11 on PDF p. 18; bridge check Q10 and Q11. Treat the methyl-carbocation example as formal electron bookkeeping only.','Correct electron allocation, ion/radical symbols and arrow directions.',16,['O-NP02','O-CP01']),
 ('Organic base · who attacks whom?','NCERT XI 8.7.2–8.7.3, PDF pp. 17–19. A nucleophile donates an electron pair; an electrophile accepts it.','Worked Problems 8.12 and 8.13; bridge check Q7, Q8, Q9 and Q12. Explain each classification in one sentence.','Recognise neutral nucleophiles as well as charged ones; identify the electron-deficient carbon.',18,['O-NP02','O-CP01']),
 ('Organic base · polarity & induction','NCERT XI 8.7.4–8.7.5, PDF pp. 19–20. Learn +I/−I, decreasing effect with distance and the simple alkyl-carbocation comparison.','Worked Problems 8.14 and 8.15; bridge check Q13 and Q15. Use only a brief hyperconjugation explanation for the alkyl comparison.','A justified simple stability order and one acidity comparison, without learning an exhaustive order list.',20,['O-NP03','O-CP01']),
 ('Organic base · resonance & acid/base reasoning','NCERT XI 8.7.6–8.7.7, PDF pp. 20–21. Move electrons, not atoms. Compare the stability of the conjugate bases.','Worked Problem 8.16; bridge check Q14, Q16 and Q17. Problem 8.17 is optional only if 8.16 is already secure.','Two valid acetate contributors and short explanations for phenol/ethanol and methylamine/ammonia.',21,['O-NP04','O-CP01']),
 ('Organic base · read a reaction','NCERT XI 8.7.10 on PDF p. 23. Recognise substitution, elimination, addition and oxidation/reduction; use the conditions written above the arrow.','Bridge check Q18, Q19 and Q20. Reattempt Q10 and Q12 for correct electron movement.','Name the reaction family and explain the arrow movement; leave full SN1/SN2 teaching for Haloalkanes.',23,['O-CP01']),
 ('Organic readiness · closed-book check','No new organic chapter today. Finish the last few minutes of the foundation lesson only if earlier segments are complete.','Bridge check Q1–20, closed-book, for 40 minutes; check answers for 10 minutes. Use the remaining minutes to identify the exact gaps.','Aim for roughly 16/20 and no persistent confusion about structures, nucleophiles/electrophiles or arrows. If below, flag those concepts for repair before Haloalkanes.',18,['O-CP01'])]

physics=[
 ('Current · Ohm, resistivity & graphs','Watch P-VS01, 03:36–30:54; read NCERT 3.2–3.7, PDF pp. 1–10. Skip 30:54–35:40 (superconductivity/Meissner).','End exercise Q3.4. Sketch one ohmic and one non-ohmic I–V curve, and label resistance versus resistivity units.','One numerical, two labelled graph sketches and a resistance/resistivity distinction.',1,['P-NP03'],['P-VS01']),
 ('Drift velocity & mobility','Watch P-VS02, 35:40–1:06:16; read the drift discussion, PDF pp. 5–8.','Examples 3.1 and 3.2 with their answers covered. Write I = neAvd and explain its quantities.','A drift calculation and an explanation of why a circuit responds quickly despite slow drift.',7,['P-NP01'],['P-VS02']),
 ('Temperature dependence','Watch P-VS03, 1:06:16–1:19:53; read NCERT 3.8.','Example 3.3, then exercises Q3.3, Q3.5 and Q3.6. Keep temperature differences and coefficient units consistent.','Four checked numerical attempts; a corrected R–T relation.',11,['P-NP01','P-NP03'],['P-VS03']),
 ('Power, EMF & terminal voltage','Watch P-VS04 and P-VS05; read NCERT 3.9–3.10, PDF pp. 12–15.','Exercises Q3.1, Q3.2 and Q3.8. For Q3.8 distinguish charging from discharging before choosing the sign of Ir.','Three attempts and a labelled EMF/terminal-voltage distinction.',12,['P-NP03'],['P-VS04','P-VS05']),
 ('Cells in series & parallel','Watch P-VS06 and P-VS07; read NCERT 3.11, PDF pp. 15–17. Do not spend time on extra maximum-current optimisation.','Derive the equivalent EMF and internal resistance for two series-aiding cells and two parallel cells; cover the derivation and reproduce it once.','Two derivations ready for the board cell-combination question on 30 October.',15,['P-BP03'],['P-VS06','P-VS07']),
 ('Kirchhoff · signs & equations','Watch P-VS08, 2:13:35–2:28:46; read NCERT 3.12.','Worked Example 3.6 with the solution covered, then end exercise Q3.7. Label assumed currents and loop directions before writing equations.','Two circuit attempts; any negative current interpreted using the original assumed direction.',19,['P-NP02','P-NP03'],['P-VS08']),
 ('Wheatstone · balance & network','Watch P-VS09 and P-VS10. Read NCERT 3.13 and show why the galvanometer current is zero at balance.','Worked Example 3.7; 2026 55/1/1 Q22 OR branch (a,b), physics pack p. 2.','Bridge condition derived and the original board network solved using its diagram.',21,['P-NP02','P-BP02'],['P-VS09','P-VS10']),
 ('Board practice · drift & cells','Recall before opening the textbook; today is independent practice, not another full lecture.','2026 55/1/1 Q20 (pack p. 1), Q31 OR branch (a,b, pack p. 3), NCERT Q3.9 and official SQP Q18 (pack p. 6).','Two board derivations, the parallel-cell calculation, one drift calculation and the electron-path explanation.',25,['P-BP01','P-BP03','P-NP03','P-BP04'],[]),
 ('Board practice · circuits & explanations','Work from the original figures. Keep claims short and link each explanation to the governing physics.','Official SQP Q9, Q10 and all parts of Q23, pack pp. 4, 5 and 7. Check with the official marking scheme; reattempt the first wrong item.','Checked circuit/power MCQs and three explanations; identify any unresolved sign or concept error.',25,['P-BP04'],[])]

solutions=[
 ('Solutions · concentration units','Read NCERT 1.1–1.2, PDF pp. 1–5. Start with n = mass/molar mass, then distinguish litres of solution from kg of solvent.','Worked Example 1.1; exercise Q1.3 and Q1.5. Show a unit beside every concentration.','Mass %, mole fraction, molarity and molality distinguished; glucose question attempted.',4,['S-NP01','S-NP04']),
 ('Solutions · conversions & ppm','Use the concentration examples, including Example 1.3 on PDF p. 5. Watch the next sequential segment of the main lesson.','Exercise Q1.8 and Q1.9. For Q1.9 explicitly convert ppm to mass percentage before calculating molality.','Two multistep attempts with denominator/units checked.',5,['S-NP01','S-NP04']),
 ('Solutions · gas solubility & Henry','Read NCERT 1.3, PDF pp. 5–8. Learn the effect of gas pressure and temperature and use the form p = KH x.','Exercise Q1.11, Q1.12 and Q1.13; official SQP Q5, solutions pack p. 5.','Henry’s law, its applications and the pressure numerical; one checked MCQ.',5,['S-NP01','S-BP05']),
 ('Solutions · Raoult & vapour pressure','Read NCERT 1.4, PDF pp. 9–13. Distinguish two volatile components from a nonvolatile solute.','Exercise Q1.16 and Q1.17. Write mole fractions and the correct form of Raoult’s law before calculating.','Two attempts plus a labelled ideal-solution vapour-pressure sketch.',9,['S-NP02']),
 ('Solutions · deviations & azeotropes','Read NCERT 1.5, PDF pp. 13–15. Connect stronger/weaker A–B interactions with deviation, heat and volume changes.','Exercise Q1.10 and Q1.14; actual PYQ Q13 and Q17, solutions pack pp. 2–3.','A positive/negative deviation comparison and two concise board explanations.',13,['S-NP02','S-BP02','S-BP03']),
 ('Solutions · boiling & freezing changes','Read the boiling/freezing parts of 1.6, PDF pp. 15–20. Relate each temperature change to molality.','Worked Examples 1.7 and 1.9 with solutions covered; exercise Q1.20. Identify why equal mass percentages need not give equal particle numbers.','Two worked models and the comparative freezing-point calculation.',17,['S-NP03','S-NP04']),
 ('Solutions · osmosis & molar mass','Read the osmotic-pressure part of 1.6, PDF pp. 20–23. Use kelvin and a consistent gas-constant unit.','Worked Example 1.11; exercise Q1.22 and Q1.30. Explain one use of osmotic pressure for molar-mass determination.','Three attempts; a usable π = CRT relation with its conditions.',22,['S-NP03','S-NP04']),
 ('Solutions · abnormal molar mass','Read NCERT 1.7, PDF pp. 23–26. Work out whether particles increase or decrease before inserting van’t Hoff factor i.','Worked Example 1.12; exercises Q1.40 and Q1.41; actual PYQ Q2, solutions pack p. 1.','Association versus dissociation distinguished, with a checked particle-count MCQ.',25,['S-NP03','S-NP04','S-BP01']),
 ('Solutions · board transfer','Finish the remaining short segment only if needed. Work independently with units, rather than copying a model answer.','Actual PYQ Q24, pack p. 4; official SQP Q25 and Q28, pack pp. 6–7 (all subparts). Check SQPs against the official marking scheme.','Association numerical, interactions/ppm and Raoult/azeotrope questions attempted and corrected.',25,['S-BP04','S-BP05'])]

revision=[
 ('Relations/functions; field & potential','Maths 65/1/1 Q32(b), PDF p. 17; Physics 55/1/1 Q1 and Q2, PDF p. 5.','Recall today’s continuity criterion, functional groups and four concentration units without notes.'),
 ('Inverse trig; capacitance','Maths Q1 and Q25(a), PDF pp. 3 and 15; Physics Q23, PDF p. 15.','Return +1 day: organic check Q5–6; maths Ex. 5.1 Q6; rewrite molarity/molality denominators.'),
 ('Matrices; Gauss’s law','Maths Q2, Q3 and Q6, PDF pp. 3 and 5; Physics Q22 original electrostatics branch (a,b), PDF p. 15.','Return +1 day: reproduce one naming example and I = neAvd; redo Solutions Q1.9(i).'),
 ('Determinants; capacitance','Maths Q4 and Q33(a), PDF pp. 5 and 19; Physics Q23, PDF p. 15, with the book closed.','Return +3 days: maths Ex. 5.1 Q3(b); organic check Q6; Solutions Q1.5 concentration units.'),
 ('Functions; field/potential','Maths Q32(b), PDF p. 17, again without the old solution; Physics Q1 and Q2, PDF p. 5.','Return +1 day: maths Ex. 5.3 Q1, organic check Q10, and the charging/discharging terminal-voltage signs.'),
 ('Inverse trig; Gauss’s law','Maths Q25(a) and Q1; Physics Q22 original electrostatics branch (a,b).','Return +3 days: Solutions SQP Q5 (Henry), organic check Q2, maths Ex. 5.2 Q2.'),
 ('Matrices; capacitance','Maths Q3 and Q6; Physics Q23. Explain your choice before calculating.','Return +3 days: reproduce organic Problem 8.11, the voltage relation for charging a cell and maths Ex. 5.3 Q5.'),
 ('Determinants; field/potential','Maths Q4 and the first incorrect step from Q33(a), or recompute A inverse if none; Physics Q1 and Q2.','Return +7 days: maths Ex. 5.1 Q6; organic check Q5–6; identify the correct denominator in Solutions Q1.5.'),
 ('Functions & inverse trig; electrostatics','Maths Q32(b) then Q25(a); Physics Q22 original electrostatics branch and explain capacitor changes in Q23 orally.','Return +7 days: organic check Q2, maths Ex. 5.1 Q17; then recall I = neAvd and the azeotrope definition.')]

days=[]
for i in range(9):
 day=date(2026,10,23)+timedelta(days=i);slots=[]
 for subject,rows,vid,book,ans,minutes in [('maths',math,'M-V01','M-N01','M-A01',75),('organic',organic,'O-V01','O-N01',None,60),('physics',physics,'P-V01','P-N01','P-A01',45),('solutions',solutions,'S-V01','S-N01','S-A01',60)]:
  row=rows[i];title,learn,pr,output,page,ids=row[:6]
  links=[res(book,'NCERT · today’s section / questions',page)]
  if ans:links.append(res(ans,'NCERT available final answers'))
  if subject=='organic':links.append(res('O-C01','Organic check · questions and answers'))
  for pid in ids:
   p=P[pid]
   if p.get('excerpt_pack_path'):
    for pg in p['excerpt_pack_pages']:
     x=dict(label=f"Board practice · pack page {pg}",url=p['excerpt_pack_path']+'#page='+str(pg))
     if x not in links:links.append(x)
   if p.get('check_with') in R:links.append(res(p['check_with'],'Official marking scheme' if '-MS' in p['check_with'] else 'NCERT answer reference'))
  clip=None
  if subject=='maths' and i<6:clip=video(vid,i*1800,min((i+1)*1800,R[vid]['duration_seconds']))
  if subject=='organic':clip=video(vid,i*1800,min((i+1)*1800,R[vid]['duration_seconds']))
  if subject=='solutions':clip=video(vid,i*2100,min((i+1)*2100,R[vid]['duration_seconds']))
  if subject=='physics':
   for segid in row[6]:
    seg=next(s for s in pool['video_segments'] if s['id']==segid)
    links.append(dict(label=seg['topic']+' · verified chapter link',url=seg['url'],resource_id='P-V01',start_seconds=seg['start_seconds'],end_seconds=seg['end_seconds']))
  elif clip:links.insert(0,dict(label=clip['label'],url=clip['url'],resource_id=vid))
  else:links.append(res(vid,'Main lesson · optional method lookup'))
  t=task(subject,title,learn,pr,output,links,ids,minutes,clip);t['id']=f'{day.isoformat()}-{subject}';t['date']=day.isoformat();t['kind']='study';t['checkpoint']='At the end, mark Done only after attempts and checking. If a step remains, record its question number for the buffer.'
  if clip:t['video_instruction']='Watch the stated sequential playback window at a comfortable speed. It is a continuation through the main lesson, not a verified topic chapter. Stop playback when that window ends; the exact NCERT section and questions below are today’s target. Record the resume time if pauses use the allotted explanation budget.'
  slots.append(t)
 title,old,new=revision[i]
 rev=task('revision','Spaced revision · '+title,'15 min maths recall/attempts, 15 min physics recall/attempts, 25 min spaced returns, then 5 min corrections/logging.',old+' '+new,'Correct the attempts; append at most three useful corrections to the linked chapter notes.',[res('M-PY01','Earlier maths · original paper'),res('P-PY01','Earlier physics · original paper'),res('M-N01','New maths · NCERT'),res('S-N01','Solutions · NCERT'),res('O-C01','Organic bridge check')],['R-M01','R-P01'],60)
 note_sets=[['relations','electrostatics','capacitance','continuity','organic','solutions'],['inverse-trig','capacitance','continuity','organic','solutions'],['matrices','electrostatics','organic','current','solutions'],['determinants','capacitance','continuity','organic','solutions'],['relations','electrostatics','continuity','organic','current'],['inverse-trig','electrostatics','solutions','organic','continuity'],['matrices','capacitance','organic','current','continuity'],['determinants','electrostatics','continuity','organic','solutions'],['relations','inverse-trig','capacitance','organic','continuity','current']]
 rev.update(id=f'{day.isoformat()}-revision',date=day.isoformat(),kind='study',recall_old=old,recall_new=new,note_ids=note_sets[i])
 # Question-page links are explicit even when the same paper is reused for recall.
 mp=[[17],[3,15],[3,5],[5,19],[17],[15,3],[5],[5,19],[17,15]][i]
 pp=[[5],[15],[15],[15],[5],[15],[15],[5],[15]][i]
 rev['resources']=[res('M-PY01',f'Earlier maths · paper PDF page {p}',p) for p in mp]+[res('P-PY01',f'Earlier physics · paper PDF page {p}',p) for p in pp]+[res('M-N01','New maths · NCERT'),res('S-N01','Solutions · NCERT'),res('O-C01','Organic bridge check')]
 slots.append(rev);days.append(dict(date=day.isoformat(),day_number=i+1,weekday=day.strftime('%a'),tasks=slots))

result=dict(phase='Phase 1',start='2026-10-23',end='2026-10-31',timezone='Asia/Kolkata',roadmap='ROADMAP.md',resource_pool='Resources/phase-01/pool.json',time_window_confirmation='pending',days=days)
(OUT/'assignments.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print('Created clock-independent assignments:',sum(len(d['tasks']) for d in days),'study tasks across',len(days),'days.')
