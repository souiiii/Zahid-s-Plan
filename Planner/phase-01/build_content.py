"""Build the revised 26 Oct–4 Nov assignments: three longer subjects + revision."""
from pathlib import Path
from datetime import date, timedelta
import copy, json, re
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent
pool=json.loads((ROOT/'Resources/phase-01/pool.json').read_text())
R={r['id']:r for r in pool['resources']}
lib=json.loads((OUT/'topic-library.json').read_text())

def res(rid,label,page=None):
 r=R[rid];url=r.get('path') or r['url']
 if rid=='O-C01':url='Resources/phase-01/organic-bridge-check.html'
 if page:url+='#page='+str(page)
 result=dict(label=label,url=url,resource_id=rid)
 if r.get('path') and r.get('url'):result['public_url']=r['url']+(f'#page={page}' if page else '')
 return result

def pack(subject,pages):
 return [dict(label=f'Board pack · p. {p}',url=f'Resources/phase-01/{subject}-board-practice.pdf#page={p}') for p in pages]

def video(subject):
 rid={'maths':'M-V01','organic':'O-V01','solutions':'S-V01'}[subject]
 return res(rid,'Video · matching topic only')

def unique(items):
 return list({x['url']:x for x in items}.values())

def task(subject,title,learn,practice,finish,bookpage,questionpages,indices,packpages=(),segments=(),budget=(10,40,40,15),recall=None,extra=None):
 rid={'maths':'M-N01','organic':'O-N01','physics':'P-N01','solutions':'S-N01'}[subject]
 book=res(rid,f'NCERT · PDF p. {bookpage}',bookpage)
 learning=[book]
 if subject!='physics':learning.insert(0,video(subject))
 else:
  for sid in segments:
   seg=next(x for x in pool['video_segments'] if x['id']==sid)
   learning.insert(len(learning)-1,dict(label='Video · '+seg['topic'],url=seg['url'],resource_id='P-V01',start_seconds=seg['start_seconds'],end_seconds=seg['end_seconds']))
 practice_links=[res(rid,f'NCERT questions · PDF p. {p}',p) for p in questionpages]+pack('solutions' if subject=='solutions' else subject,packpages)
 if subject=='organic':practice_links.append(res('O-C01','Bridge questions → answers'))
 checking=[]
 aid={'maths':'M-A01','physics':'P-A01','solutions':'S-A01'}.get(subject)
 if aid:checking.append(res(aid,'NCERT final answers'))
 if subject=='organic':checking.append(res('O-C01','Check bridge answers'))
 if any(p in {'maths':[4,5],'physics':[4,5,6,7],'solutions':[5,6,7]}.get(subject,[]) for p in packpages):checking.append(res({'maths':'M-MS01','physics':'P-MS01','solutions':'S-MS01'}[subject],'Official SQP marking scheme'))
 if extra:practice_links+=extra
 ids=[]
 for i in indices:
  ids+=lib[subject][i]['pool_practice_ids']
 if subject=='organic':ids+=['O-CP01']
 if any(p in {'maths':[1,2,3],'physics':[1,2,3],'solutions':[1,2,3,4]}.get(subject,[]) for p in packpages):
  finish+=' Actual PYQ key is not supplied; ask AI if the working is uncertain.'
 steps=[dict(title='Recall',minutes=budget[0],instruction=recall or 'Without notes, recall the last lesson. Repair one recorded error before new work.',resources=[]),
        dict(title='Learn',minutes=budget[1],instruction=learn,resources=learning),
        dict(title='Practise',minutes=budget[2],instruction=practice,resources=unique(practice_links)),
        dict(title='Check & record',minutes=budget[3],instruction=finish,resources=unique(checking))]
 return dict(subject=subject,title=title,kind='study',steps=steps,learn=learn,practice=practice,output=finish,
             resources=unique([r for st in steps for r in st['resources']]),pool_practice_ids=list(dict.fromkeys(ids)),
             pause_minutes=5,recall_prompt=recall or title,recall_item=practice.split(';')[0],note_ids=[{'maths':'continuity','organic':'organic','physics':'current','solutions':'solutions'}[subject]])

math=[]
for i,old in enumerate(lib['maths']):
 practice=old['practice']; title=old['title']; pages=[[13],[14,15],[19],[22],[27,31],[31],[34],[36,37],[41,42]][i]
 pps={1:[1],3:[1],7:[2],8:[3]}.get(i,[])
 if i==8:
  practice='Miscellaneous Q7, Q12 and Q17; 2026 paper 65/1/2 Q32 (board pack p. 3). Attempt without a model answer.'
 learn=old['learn'].replace('Finish the main lesson if needed. ','')
 learn=re.sub(r' The video is optional lookup today\.', '', learn)
 learn+=' Use the matching video OR the worked example; pause for 5 minutes halfway through this block.'
 if i==0:learn='Confirm the bridge check from 24–25 Oct, then NCERT 5.2 (PDF pp. 1–13): LHL, RHL and f(a). Use the continuity video only for this topic; take a 5-minute pause.'
 t=task('maths',title,learn,practice,'Check the answers and working. Reattempt the first wrong item; record any unfinished question number.',
        int(re.search(r'#page=(\d+)',next(r['url'] for r in old['resources'] if r.get('resource_id')=='M-N01'))[1]),pages,[i],pps,
        budget=(10,40,40,15),recall='Recall yesterday’s method. If basic algebra or limits block the first question, use the bridge guide for these 10 minutes.' if i==0 else None,
        extra=[res('M-C01','Maths prerequisite guide')] if i==0 else None)
 if i==8:t['pool_practice_ids']=[x for x in t['pool_practice_ids'] if x!='M-BP04']
 math.append(t)
math.append(task('maths','Continuity & derivatives · final board check','Recall continuity, chain/implicit/log/parametric rules. Read only the worked example for a method you cannot recall; take a 5-minute pause.',
 'Official SQP Q8 and Q22 (board pack pp. 4–5). Then redo one incorrect question from each weak method in this phase.',
 'Check SQPs with the official marking scheme. List any method still needing help before Applications of Derivatives.',41,[41,42],[8],[4,5],budget=(10,15,60,20)))
math[-1]['pool_practice_ids']=['M-BP04']

organic_specs=[
 ('Naming · chain and numbering','NCERT XI 8.5, PDF pp. 7–12. Choose the parent chain, principal group and numbering. Use only this topic in the foundation video.',
  'Cover and attempt Problems 8.7 and 8.8; Bridge Q1–2. Name each structure, then draw the structure back from its name.',10,[10,11],[1]),
 ('Structures, isomers & carbon types','NCERT XI 8.5.4 and selected 8.6, PDF pp. 13–16. Learn chain/position/functional isomers and 1°, 2°, 3° carbons.',
  'Problem 8.9; Bridge Q2, Q4 and Q19. Draw ethanol/dimethyl ether and label ortho/meta/para positions on benzene.',13,[13,15],[2]),
 ('Bond breaking & intermediates','NCERT XI 8.7.1, PDF pp. 16–18. Compare homolytic/heterolytic cleavage and recognise cations, anions and radicals.',
  'Cover Problem 8.11 and attempt it; Bridge Q10–11. Redraw the arrows with electron pairs/dots shown.',16,[16,17,18],[3]),
 ('Nucleophiles, electrophiles & arrows','NCERT XI 8.7.2–8.7.3, PDF pp. 17–19. Track which species donates and which accepts an electron pair.',
  'Problems 8.12–8.13; Bridge Q7–9 and Q12. Give one reason for each classification, then redraw the protonation arrow.',18,[18,19],[4]),
 ('Bond polarity & inductive effect','NCERT XI 8.7.4–8.7.5, PDF pp. 19–20. Learn +I/−I and why the effect weakens with distance.',
  'Problems 8.14–8.15; Bridge Q9 and Q15. Show the C–Br polarity and explain the acid comparison using the conjugate base.',20,[19,20],[5]),
 ('Simple carbocation stability','Use NCERT XI PDF pp. 20–22 for the simple alkyl-carbocation comparison. Learn only the electron-donation/hyperconjugation reason needed here.',
  'Bridge Q13, then Q10 and Q12. Draw the four alkyl carbocations, rank them, and give one reason; no exhaustive stability lists.',20,[20,21,22],[5]),
 ('Resonance · move electrons only','NCERT XI 8.7.6–8.7.7, PDF pp. 20–21. Keep atoms fixed when drawing contributors.',
  'Cover and attempt Problem 8.16; Bridge Q14. Draw acetate contributors twice from memory and check charges, octets and fixed atom positions.',21,[20,21],[6]),
 ('Acidity & basicity · limited comparisons','Use the resonance and inductive explanations on NCERT XI PDF pp. 20–21. Compare conjugate-base stability; add no full acidity/basicity ranking course.',
  'Bridge Q15–17. Explain chloroacetic/acetic acid, phenol/ethanol and methylamine/ammonia in two lines each; redo the weakest explanation.',21,[20,21],[6]),
 ('Reaction families & conditions','NCERT XI 8.7.10, PDF p. 23. Recognise substitution, elimination, addition and oxidation/reduction from reagents and products.',
  'Bridge Q18–20; then Q10 and Q12. Name each reaction family and explain both electron-pair arrows in Q20.',23,[23],[7]),
 ('Organic readiness · check and repair','Recall naming, electron pairs, induction and resonance; no new organic chapter today.',
  'Bridge Q1–20 closed-book for 40 minutes. Check for 10 minutes, then repair only the incorrect prerequisites.',18,[18,20,21],[8])]
organic=[]
for i,(title,learn,practice,page,pages,indices) in enumerate(organic_specs):
 t=task('organic',title,learn+' Take a 5-minute pause inside the learning time.',practice,
 'Check the named examples/bridge answers. Write one corrected rule and the exact item still unclear; do not copy the full lesson.',page,pages,indices,budget=(10,35,30,15),recall='Recall the structures/bonds covered on 23 Oct; redo Bridge Q5–6 orally.' if i==0 else None)
 if i==9:
  t['steps']=[dict(title='Recall',minutes=10,instruction='Recall the main prerequisite rules; take a 5-minute pause.',resources=[]),
              dict(title='Test',minutes=40,instruction='Attempt Bridge Q1–20 closed-book.',resources=[res('O-C01','Readiness questions')]),
              dict(title='Check',minutes=10,instruction='Open the answer check and mark the exact gaps.',resources=[res('O-C01','Bridge answers')]),
              dict(title='Repair',minutes=30,instruction='Redo incorrect items using NCERT. Aim near 16/20 with naming, nucleophiles and arrows clear; otherwise flag help before Haloalkanes.',resources=[res('O-N01','NCERT · prerequisites',18)])]
  t['resources']=unique([r for st in t['steps'] for r in st['resources']])
 organic.append(t)

physics=[
 task('physics','Drift, mobility & temperature','Video segments P-VS02–03; NCERT pp. 5–11. Explain I = neAvd, mobility and the linear R–T relation. Take a 5-minute pause.',
      'Cover and attempt Examples 3.1–3.3; exercises Q3.3, Q3.5 and Q3.6.',
      'Check numerical results, coefficient units and the meaning of drift velocity. Record one sign/unit mistake.',7,[7,8,11,25,26],[1,2],segments=['P-VS02','P-VS03']),
 task('physics','Power, EMF, terminal voltage & cells','NCERT 3.9–3.11, PDF pp. 12–17; matching video segments only. Skip maximum-current optimisation; take a 5-minute pause.',
      'Q3.1, Q3.2 and Q3.8. Then derive equivalent EMF/internal resistance for two series-aiding cells and two parallel cells.',
      'Check units and charging/discharging signs. Reproduce the weakest derivation without the text.',12,[12,15,16,17,25,26],[3,4],segments=['P-VS04','P-VS05','P-VS06','P-VS07']),
 task('physics','Kirchhoff & Wheatstone circuits','NCERT 3.12–3.13, PDF pp. 18–22; matching video segments. Label currents and loop directions; take a 5-minute pause.',
      'Worked Examples 3.6–3.7 with answers covered; Q3.7; 2026 Q22 OR (a,b), board pack p. 2.',
      'Check the equations and bridge condition. Explain negative current using the original assumed direction.',19,[19,20,21,22,26],[5,6],[2],segments=['P-VS08','P-VS09','P-VS10'],budget=(10,30,50,15)),
 task('physics','Board practice · drift & cells','Recall I = neAvd and the cell-combination formulas. Look up only a missing step; take a 5-minute pause.',
      '2026 Q20 (pack p. 1), Q31 OR (a,b; p. 3), NCERT Q3.9, official SQP Q18 (p. 6).',
      'Check SQP Q18 with its marking scheme. Use NCERT to check derivation steps; redo the first wrong item.',25,[26],[7],[1,3,6],budget=(10,15,60,20)),
 task('physics','Board practice · circuits & explanations','Recall power, Kirchhoff signs and Wheatstone balance. Take a 5-minute pause before the question set.',
      'Official SQP Q9, Q10 and all parts of Q23 (pack pp. 4, 5, 7). Then retry the first incorrect circuit question from this phase.',
      'Check the official marking scheme; list unresolved signs, circuits or explanation points before Magnetism.',25,[25,26],[8],[4,5,7],budget=(10,10,60,25))]

solutions=[
 task('solutions','Concentration units & conversions','NCERT 1.1–1.2, PDF pp. 1–5. Learn n = mass/molar mass, mass %, mole fraction, M, m and ppm. Use the matching video; take a 5-minute pause.',
      'Worked Examples 1.1 and 1.3 with answers covered; Q1.3, Q1.5, Q1.8 and Q1.9.',
      'Check units and whether the denominator is solution volume or solvent mass. Correct the first wrong conversion.',4,[4,5,27,28],[0,1]),
 task('solutions','Henry’s law & Raoult’s law','NCERT 1.3–1.4, PDF pp. 5–13. Use p = KH x and choose the Raoult form for volatile/nonvolatile solute. Take a 5-minute pause.',
      'Q1.11–1.13, Q1.16–1.17; official SQP Q5 (pack p. 5). Sketch ideal-solution vapour pressure.',
      'Check Q5 with its marking scheme; verify mole fractions, pressure units and temperature trends.',5,[5,9,28],[2,3],[5]),
 task('solutions','Deviations, azeotropes, boiling & freezing','NCERT 1.5–1.6, PDF pp. 13–20. Link interactions to deviation; learn ΔTb = Kb m and ΔTf = Kf m. Take a 5-minute pause.',
      'Q1.10, Q1.14; 2026 Q13 and Q17 (pack pp. 2–3); Examples 1.7 and 1.9; Q1.20.',
      'Check signs, particle counts and both board explanations. Record any wrong comparison.',13,[13,17,20,28],[4,5],[2,3],budget=(10,35,45,15)),
 task('solutions','Osmosis & abnormal molar mass','NCERT 1.6–1.7, PDF pp. 20–26. Learn π = CRT and decide whether i increases or decreases. Take a 5-minute pause.',
      'Examples 1.11–1.12; Q1.22, Q1.30, Q1.40–1.41; 2026 Q2 (pack p. 1).',
      'Check kelvin, R units, association/dissociation and the particle-count MCQ. Redo one error.',22,[22,25,26,29,30],[6,7],[1]),
 task('solutions','Solutions · board check','Recall concentration, Raoult/Henry and colligative formulas. Look up only the missing rule; take a 5-minute pause.',
      '2026 Q24 (pack p. 4); official SQP Q25 and Q28, all subparts (pack pp. 6–7).',
      'Check SQPs with their marking scheme. Correct the association numerical and note unresolved methods before Kinetics.',25,[28,29,30],[8],[4,6,7],budget=(10,10,60,25))]

older=[
 ('Relations & fields','Maths 65/1/1 Q32(b), PDF p. 17; Physics 55/1/1 Q1–2, PDF p. 5.',17,5,['relations','electrostatics']),
 ('Inverse trig & capacitance','Maths Q1 and Q25(a), PDF pp. 3,15; Physics Q23, PDF p. 15.',3,15,['inverse-trig','capacitance']),
 ('Matrices & Gauss’s law','Maths Q2–3, PDF p. 3; Physics Q22 original electrostatics branch, PDF p. 15.',3,15,['matrices','electrostatics']),
 ('Determinants & capacitance','Maths Q4, PDF p. 5, then set up Q33(a), PDF p. 19; Physics Q23, PDF p. 15.',5,15,['determinants','capacitance'])]
reported=[dict(date='2026-10-23',subject=s,title=lib[s][0]['title'],status='reported_completed',practice_verified=False,pool_practice_ids=lib[s][0]['pool_practice_ids']) for s in ['physics','organic']]
days=[];history=[dict(date=date(2026,10,23),task=lib[s][0]) for s in ['physics','organic']]
for i in range(10):
 d=date(2026,10,26)+timedelta(days=i)
 middle=copy.deepcopy((physics if i%2==0 else solutions)[i//2])
 tasks=[copy.deepcopy(math[i]),middle,copy.deepcopy(organic[i])]
 for t in tasks:t.update(id=f'v2-{d.isoformat()}-{t["subject"]}',date=d.isoformat())
 label,text,mp,pp,notes=older[i%4]
 returns=[];return_links=[];noteids=list(notes)
 for gap in [7,3,1]:
  candidates=[h for h in history if (d-h['date']).days==gap]
  for h in candidates[:2 if gap==7 else 1]:
   t=h['task'];item=t.get('recall_item') or t['practice'].split(';')[0]
   returns.append(f'{h["date"].strftime("%d %b")} · {t["subject"]}: recall {t["title"]}; retry one item from {item}')
   return_links += [r for r in t.get('resources',[]) if r.get('resource_id') in ['M-N01','P-N01','S-N01','O-N01']][:1]
   if t['subject']=='organic':return_links.append(res('O-C01','Bridge questions → answers'))
   noteids+=t.get('note_ids',[])
 returns=returns[:4]
 if not returns:returns=['Recall the organic structures and Ohm/resistivity work reported on 23 Oct.']
 olds=[res('M-PY01',f'Maths paper · PDF p. {mp}',mp),res('P-PY01',f'Physics paper · PDF p. {pp}',pp)]
 if i%4==1:olds.append(res('M-PY01','Maths Q25(a) · PDF p. 15',15))
 if i%4==3:olds.append(res('M-PY01','Maths Q33(a) · PDF p. 19',19))
 revsteps=[dict(title='Older chapters',minutes=20,instruction=text+' Allow 10 minutes per subject; attempt before checking.',resources=olds),
           dict(title='Spaced return',minutes=20,instruction='\n'.join(returns)+'\nUse about 5 minutes per return. If a listed lesson is unfinished, repair it instead.',resources=unique([r for r in return_links if r.get('resource_id') in ['M-N01','P-N01','S-N01','O-N01','O-C01']])[:4]),
           dict(title='Correct & log',minutes=5,instruction='Check the linked recall cards. Save at most three corrections; record the exact unfinished question.',resources=[],note_ids=list(dict.fromkeys(noteids)))]
 rev=dict(id=f'v2-{d.isoformat()}-revision',date=d.isoformat(),subject='revision',title='Revision · '+label,kind='study',steps=revsteps,
          learn=revsteps[0]['instruction'],practice=revsteps[1]['instruction'],output=revsteps[2]['instruction'],resources=unique([r for st in revsteps for r in st['resources']]),
          pool_practice_ids=['R-M01','R-P01'],pause_minutes=0,note_ids=list(dict.fromkeys(noteids)),return_dates=sorted({h['date'].isoformat() for h in history if (d-h['date']).days in [1,3,7]}))
 tasks.append(rev);days.append(dict(date=d.isoformat(),day_number=i+1,weekday=d.strftime('%a'),tasks=tasks))
 history += [dict(date=d,task=t) for t in tasks if t['subject']!='revision']
result=dict(schema_version=2,revision='2026-10-23-restart',phase='Phase 1',start=days[0]['date'],end=days[-1]['date'],timezone='Asia/Kolkata',roadmap='ROADMAP.md',resource_pool='Resources/phase-01/pool.json',reported_completed=reported,preparation_dates=['2026-10-24','2026-10-25'],days=days)
(OUT/'assignments.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print('Revised assignments:',len(days),'days; 3 subjects + revision per day.')
