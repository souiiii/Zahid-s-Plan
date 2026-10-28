(() => {
  'use strict';
  const data = window.PLANNER_DATA;
  const practice = window.PRACTICE_DATA;
  if (!data || !practice) return;
  const $ = (id) => document.getElementById(id);
  const escapeHTML = (value) => String(value).replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const STORAGE_KEY = 'zahid-stage-01-progress-v1';
  const slotMap = new Map(data.slots.map((slot) => [slot.id, slot]));
  let storageAvailable = true;
  function loadState() {
    try {
      const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}') || {};
      return {
        completed: new Set(Array.isArray(saved.completed) ? saved.completed.filter((id) => slotMap.has(id)) : []),
        steps: saved.steps && typeof saved.steps === 'object' && !Array.isArray(saved.steps) ? saved.steps : {},
        notes: saved.notes && typeof saved.notes === 'object' && !Array.isArray(saved.notes) ? saved.notes : {}
      };
    } catch { storageAvailable = false; return {completed:new Set(), steps:{}, notes:{}}; }
  }
  const state = loadState();
  const today = new Intl.DateTimeFormat('en-CA', {timeZone:'Asia/Kolkata',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
  let selectedDate = data.days.find((day) => day.date === today)?.date || data.days[0].date;
  let activeSlot = data.slots.find((slot) => slot.date === selectedDate);
  const expanded = new Map();
  const dialog = $('resource-dialog');
  let resourceTrigger = null;
  let currentPractice = null;
  let printOpen = [];
  function save() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({completed:[...state.completed],steps:state.steps,notes:state.notes}));
      storageAvailable = true;
    } catch { storageAvailable = false; }
    $('save-status').textContent = storageAvailable ? 'Your progress saves on this device.' : 'Saving is unavailable. Keep this page open to retain your progress.';
  }
  function checkedSteps(slot) {
    return new Set((Array.isArray(state.steps[slot.id]) ? state.steps[slot.id] : []).filter((index) => Number.isInteger(index) && index >= 0 && index < slot.steps.length));
  }
  function time(value) {
    const [hours, minutes] = value.split(':').map(Number);
    return `${hours % 12 || 12}:${String(minutes).padStart(2,'0')} ${hours >= 12 ? 'pm' : 'am'}`;
  }
  function duration(step) {
    return step.kind === 'break' ? step.duration.split('–').map(time).join('–') : step.duration;
  }
  function nextSession() {
    const incomplete = data.slots.filter((slot) => !state.completed.has(slot.id));
    return incomplete.find((slot) => checkedSteps(slot).size) || incomplete.find((slot) => slot.date >= today) || incomplete[0];
  }
  function renderProgress() {
    const count = state.completed.size;
    $('progress-label').textContent = `${count} of ${data.slots.length} sessions complete`;
    $('progress-fill').style.width = `${count / data.slots.length * 100}%`;
    document.querySelector('.progress-track').setAttribute('aria-valuenow',count);
    const next = nextSession();
    $('continue-button').disabled = !next;
    $('continue-button').innerHTML = next ? `${count || data.slots.some((slot) => checkedSteps(slot).size) ? 'Continue studying' : 'Start studying'} <span aria-hidden="true">↗</span>` : 'Week complete ✓';
  }
  function renderTabs() {
    $('day-tabs').innerHTML = data.days.map((day) => {
      const done = data.slots.filter((slot) => slot.date === day.date && state.completed.has(slot.id)).length;
      return `<button type="button" class="day-tab" role="tab" id="day-${day.date}" aria-controls="day-panel" aria-selected="${day.date === selectedDate}" tabindex="${day.date === selectedDate ? 0 : -1}" data-date="${day.date}" aria-label="${escapeHTML(day.fullLabel)}, ${done} of 2 sessions complete"><span>${day.weekday}</span><strong>${Number(day.date.slice(-2))}</strong>${done ? '<span class="day-dot" aria-hidden="true"></span>' : ''}</button>`;
    }).join('');
    $('day-panel').setAttribute('aria-labelledby',`day-${selectedDate}`);
  }
  function renderCards() {
    const day = data.days.find((item) => item.date === selectedDate);
    $('day-title').textContent = day.fullLabel.split(' · ')[0]+', '+Number(selectedDate.slice(-2))+' Nov';
    $('session-list').innerHTML = data.slots.filter((slot) => slot.date === selectedDate).map((slot) => {
      const complete = state.completed.has(slot.id);
      return `<button type="button" class="session-card ${slot.subject.toLowerCase()}" data-slot-id="${slot.id}" aria-pressed="${slot.id === activeSlot.id}" aria-controls="session-detail"><span class="subject-label">${slot.subject}</span><span class="session-card-title">${escapeHTML(slot.title)}</span><span class="session-time">${time(slot.start)}–${time(slot.end)}</span><span class="card-bottom"><span class="${complete ? 'card-complete' : ''}">${complete ? '✓ Complete' : `${checkedSteps(slot).size} of ${slot.steps.length} steps done`}</span><span class="arrow" aria-hidden="true">↗</span></span></button>`;
    }).join('');
  }
  function resourcesHTML(step,index) {
    return step.resources.map((resource,i) => `<button type="button" class="resource-button" data-resource="${index}:${i}"><span class="resource-symbol" aria-hidden="true">${resource.type === 'video' ? '▷' : resource.type === 'pdf' ? '▤' : '↗'}</span><span>${escapeHTML(resource.label)}</span></button>`).join('');
  }
  function renderDetail() {
    const slot = activeSlot;
    const checked = checkedSteps(slot);
    const complete = state.completed.has(slot.id);
    if (!expanded.has(slot.id)) expanded.set(slot.id,new Set([slot.steps.findIndex((_,i) => !checked.has(i))]));
    const open = expanded.get(slot.id);
    $('session-detail').className = `session-detail ${slot.subject.toLowerCase()}`;
    $('session-detail').innerHTML = `<header class="session-header"><div class="session-header-top"><span class="subject-label">${slot.subject}</span><span>${slot.period === 'morning' ? 'Daytime session' : 'Evening session'}</span></div><h2 id="session-title">${escapeHTML(slot.title)}</h2><div class="session-meta"><span>${time(slot.start)}–${time(slot.end)}</span><span>${slot.focusMinutes/60} study hours + a 15 min break</span></div></header>
      <ol class="step-list">${slot.steps.map((step,i) => `<li class="step-item${checked.has(i) ? ' is-checked' : ''}${step.kind === 'break' ? ' break-step' : ''}"><input type="checkbox" class="step-check" data-step="${i}" aria-label="Mark step ${i+1} complete: ${escapeHTML(step.title)}" ${checked.has(i) ? 'checked' : ''}><details data-detail="${i}" ${open.has(i) ? 'open' : ''}><summary><span class="step-title">${escapeHTML(step.title)}</span><span class="step-duration">${escapeHTML(duration(step))}</span><span class="chevron" aria-hidden="true">⌄</span></summary><div class="step-content"><p>${escapeHTML(step.description)}</p>${step.resources.length ? `<div class="resource-list">${resourcesHTML(step,i)}</div>` : ''}</div></details></li>`).join('')}</ol>
      <div class="session-bottom"><div class="done-box"><h3>You’re done when…</h3><p>${escapeHTML(slot.output)}</p></div><div class="session-actions"><button type="button" class="button ${complete ? 'button-secondary' : 'button-primary'}" id="complete-session">${complete ? 'Completed · Undo' : 'Mark session complete'}</button><button type="button" class="text-button" id="next-session" ${data.slots.indexOf(slot) === data.slots.length-1 ? 'disabled' : ''}>Next session <span aria-hidden="true">→</span></button></div><details class="note-area" ${state.notes[slot.id] ? 'open' : ''}><summary>Notes for next time</summary><label for="session-notes">What would you like to revisit?</label><textarea id="session-notes" placeholder="e.g. Exercise 6.1, question 7 — try the setup again.">${escapeHTML(typeof state.notes[slot.id] === 'string' ? state.notes[slot.id] : '')}</textarea></details></div>`;
  }
  function render() { renderTabs(); renderCards(); renderDetail(); renderProgress(); }
  function selectDay(date,focusTab=false) {
    if (!data.days.some((day) => day.date === date)) return;
    selectedDate = date;
    activeSlot = data.slots.find((slot) => slot.date === date);
    render();
    if (focusTab) $(`day-${date}`).focus({preventScroll:true});
  }
  function selectSlot(id, focus=false) {
    const slot = slotMap.get(id);
    if (!slot) return;
    activeSlot = slot; selectedDate = slot.date; render();
    if (focus) { $('session-detail').focus({preventScroll:true}); $('session-detail').scrollIntoView({block:'start'}); }
  }
  function showReader(title,kind,html) {
    $('resource-title').textContent = title;
    $('resource-kind').textContent = kind;
    $('resource-content').innerHTML = html;
    if (!dialog.open) {resourceTrigger = document.activeElement; dialog.showModal();}
    dialog.scrollTop = 0;
    $('close-resource').focus({preventScroll:true});
  }
  function practiceConstants(id) {
    if (id === 'm0' || id === 'mcheck' || id === 'repair') return '';
    return `<details class="constants"><summary>Constants you may need</summary><p>${id.startsWith('p') ? 'μ₀ = 4π × 10⁻⁷ T m A⁻¹; e = 1.60 × 10⁻¹⁹ C; proton mass = 1.67 × 10⁻²⁷ kg.' : 'F = 96500 C mol⁻¹. At 298 K, use 0.0591 V in the base-10 Nernst equation.'}</p></details>`;
  }
  function showPractice(id) {
    const item = practice[id];
    if (!item) return;
    currentPractice = id;
    showReader(item.title,'Practice',`<p class="practice-meta">${item.meta}</p>${item.answers ? '<p class="reader-note">Try this on paper without your notes or a calculator. Show your working, then check the answers below.</p>' : ''}${practiceConstants(id)}${item.questions}${item.answers ? `<details class="answer-details"><summary>Show answers & marking guide</summary><div>${item.answers}</div></details>` : ''}<button type="button" class="text-button" data-library>All practice & answers →</button>`);
  }
  function showLibrary(answers=false) {
    showReader(answers ? 'Check your answers' : 'Practice & answers','Your resources',`<p class="reader-note">${answers ? 'Choose the practice you want to check. Answers are below the questions.' : 'Choose a warm-up or a chapter test. Each one includes its answers.'} These are practice questions, not official exam papers.</p><div class="library-list">${Object.entries(practice).map(([id,item]) => `<button type="button" class="library-item" data-practice="${id}"><span>${escapeHTML(item.title)}<small>${item.meta}</small></span><span aria-hidden="true">↗</span></button>`).join('')}</div>`);
  }
  function matchingPractice() {
    if (currentPractice && currentPractice !== 'repair' && practice[currentPractice]?.title.toLowerCase().includes(activeSlot.subject.toLowerCase())) return currentPractice;
    const exercise = activeSlot.steps.flatMap((step) => step.resources).find((resource) => resource.type === 'check');
    return exercise ? exercise.url.split('#')[1] : null;
  }
  function openResource(resource) {
    if (resource.type === 'check') return showPractice(resource.url.split('#')[1]);
    if (resource.type === 'key') {
      if (resource.url.endsWith('#repair')) return showPractice('repair');
      const id = matchingPractice();
      if (id) {
        showPractice(id);
        const answers = document.querySelector('.answer-details');
        if (answers) { answers.open = true; answers.scrollIntoView({block:'start'}); }
        return;
      }
      return showLibrary(true);
    }
    if (resource.type === 'video') {
      const url = new URL(resource.url);
      const start = parseInt(url.searchParams.get('t') || '0',10);
      showReader(resource.label,'Video lesson',`<iframe class="video-frame" src="https://www.youtube-nocookie.com/embed/${escapeHTML(url.searchParams.get('v'))}?start=${start}&rel=0" title="${escapeHTML(resource.label)}" allow="encrypted-media; picture-in-picture; fullscreen" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe><p class="reader-note">The lesson starts at the selected topic. Videos need an internet connection. If playback is unavailable, close this reader and use the textbook in the same step.</p>`);
      return;
    }
    showReader(resource.label,'NCERT textbook',`<iframe class="pdf-frame" src="${escapeHTML(resource.url)}" title="${escapeHTML(resource.label)}"></iframe><a class="resource-download" href="${escapeHTML(resource.url.split('#')[0])}" download>Download this textbook</a><p class="reader-note">The reader opens at the assigned page. If your browser cannot display the PDF, download it to read on your device.</p>`);
  }
  document.addEventListener('click', (event) => {
    const target = event.target.closest('button');
    if (!target) return;
    if (target.dataset.date) return selectDay(target.dataset.date,true);
    if (target.dataset.slotId) {
      const compact = window.matchMedia('(max-width: 760px)').matches;
      selectSlot(target.dataset.slotId, compact);
      if (!compact) document.querySelector(`[data-slot-id="${activeSlot.id}"]`).focus({preventScroll:true});
      return;
    }
    if (target.dataset.resource) {const [step,index] = target.dataset.resource.split(':').map(Number); return openResource(activeSlot.steps[step].resources[index]);}
    if (target.dataset.practice) return showPractice(target.dataset.practice);
    if (target.hasAttribute('data-library') || target.id === 'practice-library') return showLibrary();
    if (target.id === 'close-resource') return dialog.close();
    if (target.id === 'continue-button') {const next=nextSession(); if(next) selectSlot(next.id,true); return;}
    if (target.id === 'next-session') {const next=data.slots[data.slots.indexOf(activeSlot)+1]; if(next) selectSlot(next.id,true); return;}
    if (target.id === 'complete-session') {
      if (state.completed.has(activeSlot.id)) state.completed.delete(activeSlot.id); else state.completed.add(activeSlot.id);
      save(); render(); $('complete-session').focus({preventScroll:true});
    }
  });
  document.addEventListener('change',(event) => {
    if (!event.target.matches('[data-step]')) return;
    const index=Number(event.target.dataset.step), checked=checkedSteps(activeSlot);
    if(event.target.checked) checked.add(index); else {checked.delete(index); state.completed.delete(activeSlot.id);}
    state.steps[activeSlot.id]=[...checked];
    event.target.closest('.step-item').classList.toggle('is-checked',event.target.checked);
    // Keep the open lesson and keyboard focus stable while progress updates.
    const completed=state.completed.has(activeSlot.id);
    $('complete-session').textContent=completed?'Completed · Undo':'Mark session complete';
    $('complete-session').className=`button ${completed?'button-secondary':'button-primary'}`;
    save(); renderCards(); renderTabs(); renderProgress();
  });
  document.addEventListener('input',(event) => {if(event.target.id==='session-notes'){state.notes[activeSlot.id]=event.target.value;save();}});
  $('session-detail').addEventListener('toggle',(event) => {
    if(!event.target.matches('[data-detail]'))return;
    const index=Number(event.target.dataset.detail), open=expanded.get(activeSlot.id);
    if(open){if(event.target.open)open.add(index);else open.delete(index);}
  },true);
  $('day-tabs').addEventListener('keydown',(event) => {
    if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;
    event.preventDefault();
    const index=data.days.findIndex((day)=>day.date===selectedDate);
    const next=event.key==='Home'?0:event.key==='End'?6:(index+(event.key==='ArrowRight'?1:6))%7;
    selectDay(data.days[next].date,true);
  });
  dialog.addEventListener('click',(event)=>{if(event.target===dialog){const rect=dialog.getBoundingClientRect();if(event.clientX<rect.left||event.clientX>rect.right||event.clientY<rect.top||event.clientY>rect.bottom)dialog.close();}});
  dialog.addEventListener('close',()=>{$('resource-content').replaceChildren();if(resourceTrigger?.isConnected)resourceTrigger.focus({preventScroll:true});});
  window.addEventListener('beforeprint',()=>{printOpen=[...document.querySelectorAll('[data-detail]')].filter((item)=>!item.open);printOpen.forEach((item)=>item.open=true);});
  window.addEventListener('afterprint',()=>{printOpen.forEach((item)=>item.open=false);});
  render();
  if(!storageAvailable)$('save-status').textContent='Saving is unavailable. Keep this page open to retain your progress.';
  // Existing bookmarks to the old practice page still open the same in-page reader.
  const initialPractice=location.hash.slice(1);
  if(practice[initialPractice])showPractice(initialPractice);else if(initialPractice==='keys')showLibrary(true);
})();
