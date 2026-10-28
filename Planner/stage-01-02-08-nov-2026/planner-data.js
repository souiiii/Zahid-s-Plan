(() => {
  'use strict';

  const resource = (label, url, type = 'pdf') => ({ label, url, type });
  const book = (label, path, page = 1) => resource(label, `../../Sources/Books/${path}#page=${page}`);
  const video = (label, id, seconds) => resource(label, `https://www.youtube.com/watch?v=${id}${seconds ? `&t=${seconds}s` : ''}`, 'video');
  const check = (label, anchor) => resource(label, `#${anchor}`, 'check');

  const R = {
    m0: check('Maths warm-up', 'm0'),
    c0: check('Chemistry warm-up', 'c0'),
    p0: check('Physics warm-up', 'p0'),
    p1: check('Magnetic force practice', 'p1'),
    pCheck: check('Physics test · 20 marks', 'pcheck'),
    cCheck: check('Chemistry test · 20 marks', 'ccheck'),
    mCheck: check('Maths test · 20 marks', 'mcheck'),
    keys: resource('Check your answers', '#keys', 'key'),
    repair: resource('How to fix a mistake', '#repair', 'key'),

    neha: video('Neha · Applications of derivatives', 'hs2_sgEBH30'),
    mPrev: book('NCERT · Review derivative rules', 'maths-part-1/lemh105.pdf'),
    mRates: book('NCERT · Related rates', 'maths-part-1/lemh106.pdf'),
    mInc: book('NCERT · Increasing & decreasing functions', 'maths-part-1/lemh106.pdf', 6),
    mExt: book('NCERT · Maximum & minimum values', 'maths-part-1/lemh106.pdf', 14),
    mOpt: book('NCERT · Optimisation examples', 'maths-part-1/lemh106.pdf', 21),
    mEx1: book('NCERT · Exercise 6.1', 'maths-part-1/lemh106.pdf', 4),
    mEx2: book('NCERT · Exercise 6.2', 'maths-part-1/lemh106.pdf', 12),
    mEx3: book('NCERT · Exercise 6.3', 'maths-part-1/lemh106.pdf', 28),
    mMisc: book('NCERT · Miscellaneous exercise', 'maths-part-1/lemh106.pdf', 37),
    mAns: book('NCERT · Maths answers', 'maths-part-1/lemh1an.pdf', 12),

    pFields: book('NCERT · Magnetic field laws', 'phy-part-1/leph104.pdf', 7),
    pForce: book('NCERT · Force and motion', 'phy-part-1/leph104.pdf', 2),
    pCoils: book('NCERT · Torque & galvanometer', 'phy-part-1/leph104.pdf', 16),
    pEx: book('NCERT · Chapter 4 exercise', 'phy-part-1/leph104.pdf', 28),
    pAns: book('NCERT · Physics answers', 'phy-part-1/leph1an.pdf', 2),
    pPrev1: book('NCERT · Review electrostatics', 'phy-part-1/leph101.pdf'),
    pPrev2: book('NCERT · Review capacitance', 'phy-part-1/leph102.pdf'),
    pPrev3: book('NCERT · Review current electricity', 'phy-part-1/leph103.pdf'),
    pA: video('Arvind · Field concepts 01:05', 'd0I4JFSuUHk', 65),
    pB: video('Arvind · Long wire 30:21', 'd0I4JFSuUHk', 1821),
    pC: video('Arvind · Circular loop 58:30', 'd0I4JFSuUHk', 3510),
    pD: video('Arvind · Ampere’s law 1:52:35', 'd0I4JFSuUHk', 6755),
    pE: video('Arvind · Straight wire 2:03:41', 'd0I4JFSuUHk', 7421),
    pF: video('Arvind · Solenoid 2:25:27', 'd0I4JFSuUHk', 8727),
    pG: video('Arvind · Force & motion 2:32:07', 'd0I4JFSuUHk', 9127),
    pH: video('Arvind · Orbit derivation 3:04:23', 'd0I4JFSuUHk', 11063),
    pI: video('Arvind · Conductor force 3:24:59', 'd0I4JFSuUHk', 12299),
    pJ: video('Arvind · Wires to galvanometer 3:40:06', 'd0I4JFSuUHk', 13206),
    pK: video('Arvind · Sensitivity 4:51:35', 'd0I4JFSuUHk', 17495),
    pL: video('Arvind · Ammeter conversion 5:05:15', 'd0I4JFSuUHk', 18315),
    pM: video('Arvind · Voltmeter conversion 5:27:21', 'd0I4JFSuUHk', 19641),

    cCells: book('NCERT · Cells & potentials', 'chem-part-1/lech102.pdf'),
    cNernst: book('NCERT · Nernst & equilibrium', 'chem-part-1/lech102.pdf', 6),
    cCond: book('NCERT · Conductance & Kohlrausch', 'chem-part-1/lech102.pdf', 11),
    cElec: book('NCERT · Electrolysis', 'chem-part-1/lech102.pdf', 21),
    cBatt: book('NCERT · Batteries & corrosion', 'chem-part-1/lech102.pdf', 24),
    cEx: book('NCERT · Chapter 2 exercise', 'chem-part-1/lech102.pdf', 29),
    cAns: book('NCERT · Chemistry answers', 'chem-part-1/lech1an.pdf'),
    cA: video('Bharat · Redox recap 03:25', 'FNm0fII4heo', 205),
    cB: video('Bharat · Cells & potentials 27:00', 'FNm0fII4heo', 1620),
    cC: video('Bharat · Nernst 57:40', 'FNm0fII4heo', 3460),
    cD: video('Bharat · Conductance 1:16:10', 'FNm0fII4heo', 4570),
    cE: video('Bharat · Electrolysis 1:46:25', 'FNm0fII4heo', 6385)
  };

  const rest = (time, evening = false) => ({
    title: 'Take a break', duration: time, kind: 'break',
    description: evening ? 'Step away from the screen, drink water and rest your eyes. Come back after 15 minutes.' : 'Leave the desk, stretch and drink water. Come back after 15 minutes.',
    resources: []
  });

  window.PLANNER_DATA = {
    days: [
      { date: '2026-11-02', weekday: 'Mon', dateLabel: '02 Nov', fullLabel: 'Monday · 2 November 2026' },
      { date: '2026-11-03', weekday: 'Tue', dateLabel: '03 Nov', fullLabel: 'Tuesday · 3 November 2026' },
      { date: '2026-11-04', weekday: 'Wed', dateLabel: '04 Nov', fullLabel: 'Wednesday · 4 November 2026' },
      { date: '2026-11-05', weekday: 'Thu', dateLabel: '05 Nov', fullLabel: 'Thursday · 5 November 2026' },
      { date: '2026-11-06', weekday: 'Fri', dateLabel: '06 Nov', fullLabel: 'Friday · 6 November 2026' },
      { date: '2026-11-07', weekday: 'Sat', dateLabel: '07 Nov', fullLabel: 'Saturday · 7 November 2026' },
      { date: '2026-11-08', weekday: 'Sun', dateLabel: '08 Nov', fullLabel: 'Sunday · 8 November 2026' }
    ],
    slots: [
      {
        id: '2026-11-02-maths', date: '2026-11-02', period: 'morning', subject: 'Maths',
        title: 'Related rates of change', start: '11:30', end: '14:45', focusMinutes: 180,
        output: 'Ten exercise questions are attempted, corrections are written, and your Maths warm-up is checked.',
        steps: [
          { title: 'Try a warm-up', duration: '15 min', description: 'Try the Maths warm-up, then check your answers. If you miss two derivative questions, spend the first 20 minutes of the next step reviewing the chain and product rules in Chapter 5.', resources: [R.m0, R.keys, R.mPrev] },
          { title: 'Learn', duration: '60 min', description: 'Study rate of change and related rates with NCERT section 6.2 and Examples 1, 2 and 4. Write the chain-rule equation before substituting values.', resources: [R.neha, R.mRates] },
          { title: 'First practice', duration: '15 min', description: 'Solve Exercise 6.1 Q1 and Q3 without viewing solutions.', resources: [R.mEx1] },
          rest('13:00–13:15'),
          { title: 'Practise', duration: '65 min', description: 'Solve Exercise 6.1 Q2, Q7, Q8, Q10, Q11, Q14, Q15 and Q16. Draw ladder/cone diagrams, identify changing variables and keep units.', resources: [R.mEx1] },
          { title: 'Check and correct', duration: '20 min', description: 'Check the answers and redo the first two incorrect setups without looking.', resources: [R.mAns, R.repair] },
          { title: 'Note what’s left', duration: '5 min', description: 'Record unfinished question numbers and one reason for a mistake.', resources: [] }
        ]
      },
      {
        id: '2026-11-02-chemistry', date: '2026-11-02', period: 'evening', subject: 'Chemistry',
        title: 'Cells & electrode potential', start: '21:30', end: '23:45', focusMinutes: 120,
        output: 'Six written answers and one correct labelled cell diagram are complete.',
        steps: [
          { title: 'Try a warm-up', duration: '15 min', description: 'Try the Chemistry warm-up, then check your answers. Review molarity or balancing electrons in the next step if you need to.', resources: [R.c0, R.keys] },
          { title: 'Learn', duration: '45 min', description: 'Watch redox 03:25–12:50 and cells 27:00–57:40. Draw the Daniell cell; label anode, cathode, electron direction and salt-bridge role. Write E°cell = E°cathode − E°anode.', resources: [R.cA, R.cB, R.cCells] },
          rest('22:30–22:45', true),
          { title: 'Practise', duration: '40 min', description: 'Attempt NCERT in-text Q2.1–2.3 and end-exercise Q2.1–2.3. These are two different question lists.', resources: [R.cCells, R.cEx] },
          { title: 'Check and correct', duration: '15 min', description: 'Use the answers and NCERT potential table; fix electrode signs and reducing-power order.', resources: [R.cAns, R.cCells, R.repair] },
          { title: 'Note what’s left', duration: '5 min', description: 'Record one unresolved confusion, or “none”.', resources: [] }
        ]
      },
      {
        id: '2026-11-03-physics', date: '2026-11-03', period: 'morning', subject: 'Physics',
        title: 'Magnetic fields & circular loop', start: '11:30', end: '14:45', focusMinutes: 180,
        output: 'Field-direction rules, three core formulas and the loop-axis derivation can be reproduced without the video.',
        steps: [
          { title: 'Try a warm-up', duration: '15 min', description: 'Try the Physics warm-up, then check your answers. Note which topics need another look: electrostatics, capacitance or current electricity. You will revisit them on Sunday.', resources: [R.p0, R.keys] },
          { title: 'Learn', duration: '75 min', description: 'Watch field concepts 01:05–23:07, long wire 30:21–35:20 and circular loop 58:30–1:29:55. Pause for the right-hand rule and loop-axis derivation.', resources: [R.pA, R.pB, R.pC, R.pFields] },
          rest('13:00–13:15'),
          { title: 'Finish the concept', duration: '15 min', description: 'Watch Ampere’s law, its straight-wire application and the qualitative solenoid segments. State Ampere’s law and sketch the solenoid field.', resources: [R.pD, R.pE, R.pF] },
          { title: 'Practise', duration: '60 min', description: 'Solve end-exercise Q4.1–4.4, work through on your own Example 4.6, then reproduce the loop-axis derivation once with a labelled diagram.', resources: [R.pEx, R.pFields] },
          { title: 'Check and correct', duration: '15 min', description: 'Check answers, redo the first wrong field/direction step and note unfinished question numbers. Skip thick-cylinder derivations and Q4.8 in this pass.', resources: [R.pAns, R.repair] }
        ]
      },
      {
        id: '2026-11-03-chemistry', date: '2026-11-03', period: 'evening', subject: 'Chemistry',
        title: 'Nernst, Gibbs energy & equilibrium', start: '21:30', end: '23:45', focusMinutes: 120,
        output: 'Six worked problems show Q, n, substitutions and units.',
        steps: [
          { title: 'Learn', duration: '40 min', description: 'Watch Nernst 57:40–1:16:10, then read NCERT section 2.3.1–2.3.2 and Examples 2.2–2.3. Write the balanced reaction, Q and n before each formula.', resources: [R.cC, R.cNernst] },
          { title: 'First practice', duration: '20 min', description: 'Attempt in-text Q2.4 and Q2.5. Cover E versus E°, ΔG° = −nFE° and log K = nE°/0.0591.', resources: [R.cNernst] },
          rest('22:30–22:45', true),
          { title: 'Practise', duration: '45 min', description: 'Solve end-exercise Q2.4(i), Q2.4(ii), Q2.5(i) and Q2.5(iii), including every requested quantity.', resources: [R.cEx] },
          { title: 'Check and correct', duration: '15 min', description: 'Compare with the answers and redo one mistaken Q/n/sign/log step without the key.', resources: [R.cAns, R.repair] }
        ]
      },
      {
        id: '2026-11-04-maths', date: '2026-11-04', period: 'morning', subject: 'Maths',
        title: 'Increasing & decreasing functions', start: '11:30', end: '14:45', focusMinutes: 180,
        output: 'Each answer includes the allowed input values, a derivative sign chart and a reason for any parameter limits.',
        steps: [
          { title: 'Learn', duration: '60 min', description: 'Study NCERT section 6.3 and Examples 10–12. Find the allowed input values, differentiate, then use a sign chart to see where the function increases or decreases.', resources: [R.neha, R.mInc] },
          { title: 'First practice', duration: '30 min', description: 'Solve Exercise 6.2 Q3, Q4 and Q5, including all requested subparts.', resources: [R.mEx2] },
          rest('13:00–13:15'),
          { title: 'Practise', duration: '60 min', description: 'Solve Exercise 6.2 Q6(a), Q6(c), Q7, Q8, Q14 and Q19. State which input values are allowed and explain any limits you find for a parameter.', resources: [R.mEx2] },
          { title: 'Revisit earlier mistakes', duration: '15 min', description: 'Retry Monday’s earliest two incorrect questions. If none were incorrect, solve Exercise 6.1 Q12 and Q18.', resources: [R.mEx1] },
          { title: 'Check and correct', duration: '15 min', description: 'Check the answers, close the key and rewrite any incomplete sign chart.', resources: [R.mAns, R.repair] }
        ]
      },
      {
        id: '2026-11-04-physics', date: '2026-11-04', period: 'evening', subject: 'Physics',
        title: 'Magnetic force & circular motion', start: '21:30', end: '23:45', focusMinutes: 120,
        output: 'Two examples, two exercise questions and the direction/motion drill are written and checked.',
        steps: [
          { title: 'Learn', duration: '60 min', description: 'Watch force and motion, orbit derivation and conductor force. Write F=q(v×B), F=I(ℓ×B), r=mv/(|q|B) and T=2πm/(|q|B). Explain why speed remains constant.', resources: [R.pG, R.pH, R.pI, R.pForce] },
          rest('22:30–22:45', true),
          { title: 'Practise', duration: '45 min', description: 'Work NCERT Examples 4.1 and 4.3, end-exercise Q4.5 and Q4.6, then complete all four magnetic force practice questions.', resources: [R.pForce, R.pEx, R.p1] },
          { title: 'Check and correct', duration: '15 min', description: 'Check both answer keys and redo the first incorrect direction or orbit calculation.', resources: [R.pAns, R.keys, R.repair] }
        ]
      },
      {
        id: '2026-11-05-chemistry', date: '2026-11-05', period: 'morning', subject: 'Chemistry',
        title: 'Conductivity & Kohlrausch', start: '11:30', end: '14:45', focusMinutes: 180,
        output: 'One labelled conductivity graph, the dilution explanation and checked Kohlrausch applications are complete.',
        steps: [
          { title: 'Learn', duration: '60 min', description: 'Watch conductance 1:16:10–1:46:25, then read NCERT section 2.4. Make a unit table for R, G, cell constant, κ and Λm. Cover and rework Example 2.4.', resources: [R.cD, R.cCond] },
          { title: 'First practice', duration: '30 min', description: 'Solve end-exercise Q2.7, Q2.8 and Q2.9.', resources: [R.cEx] },
          rest('13:00–13:15'),
          { title: 'Practise', duration: '60 min', description: 'Solve end-exercise Q2.10, including its graph, and Q2.11; then in-text Q2.7–2.9. Use Λm/Λ°m for degree of dissociation where applicable.', resources: [R.cEx, R.cCond] },
          { title: 'Revisit earlier mistakes', duration: '15 min', description: 'Retry Tuesday’s earliest incorrect Nernst question. If none was incorrect, solve end-exercise Q2.5(ii).', resources: [R.cEx] },
          { title: 'Check and correct', duration: '15 min', description: 'Check answers, units, graph interpretation and calculations. Rewrite the dilution explanation in two lines.', resources: [R.cAns, R.repair] }
        ]
      },
      {
        id: '2026-11-05-maths', date: '2026-11-05', period: 'evening', subject: 'Maths',
        title: 'Maximum & minimum values', start: '21:30', end: '23:45', focusMinutes: 120,
        output: 'You have found local maximum and minimum values, compared endpoint values, and solved for a parameter using a zero derivative.',
        steps: [
          { title: 'Learn', duration: '45 min', description: 'Study NCERT section 6.4–6.4.1 and Examples 17, 19 and 27. Distinguish critical points, derivative tests and endpoint comparison. Note why f′=0 alone is insufficient.', resources: [R.neha, R.mExt] },
          { title: 'First practice', duration: '15 min', description: 'Solve Exercise 6.3 Q3(ii) and Q3(v).', resources: [R.mEx3] },
          rest('22:30–22:45', true),
          { title: 'Practise', duration: '45 min', description: 'Solve Exercise 6.3 Q3(vi), Q5(i), Q5(ii), Q7 and Q11. State the allowed input values, identify local maxima and minima, and check the endpoints for the overall maximum and minimum.', resources: [R.mEx3] },
          { title: 'Check and correct', duration: '15 min', description: 'Check the answers and add any missing endpoint or justification step.', resources: [R.mAns, R.repair] }
        ]
      },
      {
        id: '2026-11-06-physics', date: '2026-11-06', period: 'morning', subject: 'Physics',
        title: 'Parallel wires, torque & galvanometer', start: '11:30', end: '14:45', focusMinutes: 180,
        output: 'Two correctly connected meter diagrams and four worked questions are complete.',
        steps: [
          { title: 'Learn', duration: '90 min', description: 'Study force per unit length, attraction/repulsion, magnetic moment, torque, radial field and sensitivity. Derive the torque balance rather than copying the lecture.', resources: [R.pJ, R.pK, R.pCoils] },
          rest('13:00–13:15'),
          { title: 'Learn & derive', duration: '45 min', description: 'Watch both meter-conversion segments. Derive the shunt and series-resistance formulas and draw both circuits.', resources: [R.pL, R.pM, R.pCoils] },
          { title: 'Practise', duration: '35 min', description: 'Solve end-exercise Q4.7, Q4.9 and Q4.10 plus Example 4.12.', resources: [R.pEx, R.pCoils] },
          { title: 'Check and correct', duration: '10 min', description: 'Check the answers and note the step you still need to finish. Longer derivation practice is reserved for Sunday.', resources: [R.pAns, R.repair] }
        ]
      },
      {
        id: '2026-11-06-chemistry', date: '2026-11-06', period: 'evening', subject: 'Chemistry',
        title: 'Electrolysis & Faraday calculations', start: '21:30', end: '23:45', focusMinutes: 120,
        output: 'm=MIt/nF is used correctly, with one series-cell calculation and active/inert-electrode product predictions.',
        steps: [
          { title: 'Learn', duration: '40 min', description: 'Read NCERT section 2.5, both Faraday laws and Example 2.10. Use the video for products of electrolysis, capped at 15 minutes. Contrast active and inert electrodes.', resources: [R.cElec, R.cE] },
          { title: 'First practice', duration: '20 min', description: 'Solve end-exercise Q2.12 and Q2.13, including all subparts.', resources: [R.cEx] },
          rest('22:30–22:45', true),
          { title: 'Practise', duration: '45 min', description: 'Solve end-exercise Q2.14, Q2.15, Q2.16 and Q2.18. If time runs short, prioritise Q2.15 and Q2.18 and save the remaining questions for your next review.', resources: [R.cEx] },
          { title: 'Check and correct', duration: '15 min', description: 'Check the electron ratios, charge calculations and products using the textbook and answers. Redo one failed calculation.', resources: [R.cElec, R.cAns, R.repair] }
        ]
      },
      {
        id: '2026-11-07-chemistry', date: '2026-11-07', period: 'morning', subject: 'Chemistry',
        title: 'Batteries, corrosion & chapter check', start: '11:30', end: '14:45', focusMinutes: 180,
        output: 'You have checked your test or noted why you saved it for later, and listed the questions to revisit.',
        steps: [
          { title: 'Learn', duration: '45 min', description: 'Read NCERT section 2.6–2.8. Make a battery table with reactants/electrodes, reactions and rechargeable status. Draw rusting as local anodic/cathodic processes.', resources: [R.cBatt] },
          { title: 'Try from memory', duration: '25 min', description: 'Answer in-text Q2.13–2.15 from memory, then check the chapter.', resources: [R.cBatt] },
          { title: 'Work on tricky questions', duration: '20 min', description: 'Return to your first unfinished or incorrect Chemistry question. If none remains, solve exercise Q2.6.', resources: [R.cEx, R.repair] },
          rest('13:00–13:15'),
          { title: 'Test yourself', duration: '45 min', description: 'Attempt the 20-mark Electrochemistry check without your notes. If you have not studied a topic yet, learn it now and save the test for later.', resources: [R.cCheck] },
          { title: 'Mark your work and try again', duration: '30 min', description: 'Use the marking guide, note why you lost each mark and re-solve the first two incorrect questions.', resources: [R.keys, R.repair] },
          { title: 'Note what’s left', duration: '15 min', description: 'Note your score, or why you saved the test for later, and the topics you still need to practise.', resources: [] }
        ]
      },
      {
        id: '2026-11-07-maths', date: '2026-11-07', period: 'evening', subject: 'Maths',
        title: 'Optimisation word problems', start: '21:30', end: '23:45', focusMinutes: 120,
        output: 'Number-product, box, cylinder, cone and cost setups are written, with domains and maximum/minimum justification.',
        steps: [
          { title: 'Learn', duration: '30 min', description: 'Study NCERT Examples 22 and 36. Name the variables, write the constraint, and express what you want to maximise or minimise using one variable. Check its allowed values, differentiate, and justify your answer.', resources: [R.neha, R.mOpt] },
          { title: 'First practice', duration: '30 min', description: 'Solve Exercise 6.3 Q13 and Q17. Draw the open-box diagram before differentiating.', resources: [R.mEx3] },
          rest('22:30–22:45', true),
          { title: 'Practise', duration: '45 min', description: 'Solve Exercise 6.3 Q21 and Q24, then miscellaneous Q6 (minimum cost). These are three long problems, not a speed drill.', resources: [R.mEx3, R.mMisc] },
          { title: 'Check and correct', duration: '15 min', description: 'Check your equations and explain why each answer is a maximum or minimum. If a long problem is unfinished, save it for Sunday.', resources: [R.mAns, R.repair] }
        ]
      },
      {
        id: '2026-11-08-physics', date: '2026-11-08', period: 'morning', subject: 'Physics',
        title: 'Derivations & chapter check', start: '11:30', end: '14:45', focusMinutes: 180,
        output: 'You have written the derivations from memory and recorded your test score, or why you saved the test for later.',
        steps: [
          { title: 'Try from memory', duration: '60 min', description: 'From memory, write the loop-axis field, straight-wire field, rectangular-coil torque, galvanometer torque balance and both meter-conversion formulas. Compare and correct missing steps.', resources: [R.pFields, R.pCoils] },
          { title: 'Work on tricky questions', duration: '30 min', description: 'Solve exercise Q4.13 and revisit your first mistake from the Physics warm-up or this chapter. If no errors remain, reattempt Q4.10 without the key.', resources: [R.pEx, R.pPrev1, R.pPrev2, R.pPrev3] },
          rest('13:00–13:15'),
          { title: 'Test yourself', duration: '45 min', description: 'Attempt the 20-mark Moving Charges and Magnetism check without your notes. If you have not studied a topic yet, learn it now and save the test for later.', resources: [R.pCheck] },
          { title: 'Mark your work and try again', duration: '30 min', description: 'Use the marking guide and re-solve the first two incorrect questions.', resources: [R.keys, R.repair] },
          { title: 'Note what’s left', duration: '15 min', description: 'Write down the topics you covered and the question numbers you still need to finish.', resources: [] }
        ]
      },
      {
        id: '2026-11-08-maths', date: '2026-11-08', period: 'evening', subject: 'Maths',
        title: 'Derivatives test & weekly review', start: '21:30', end: '23:45', focusMinutes: 120,
        output: 'You have a short list of topics and question numbers to start with next week.',
        steps: [
          { title: 'Test yourself', duration: '45 min', description: 'Attempt the 20-mark applications of derivatives test without your notes. If you still need to learn a method, use the textbook now and save the test for later.', resources: [R.mCheck, R.mOpt] },
          { title: 'Mark', duration: '15 min', description: 'Use the marking guide. Keep the first-attempt score separate from corrections.', resources: [R.keys] },
          rest('22:30–22:45', true),
          { title: 'Check and correct', duration: '25 min', description: 'Rewrite every lost-mark step from the check without copying the key.', resources: [R.keys, R.repair] },
          { title: 'Work on tricky questions', duration: '25 min', description: 'Retry the earliest unfinished or incorrect Maths question. If none remains, solve miscellaneous Q8 (window optimisation).', resources: [R.mMisc, R.repair] },
          { title: 'Get ready for next week', duration: '10 min', description: 'For each subject, note what you learned, what you can solve on your own, your test score (or why you saved it for later), and the first question to revisit next week.', resources: [] }
        ]
      }
    ]
  };
})();
