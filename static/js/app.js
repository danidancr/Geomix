/* ═══════════════════════════════════════════════
   GEOMIX  –  app.js
   ═══════════════════════════════════════════════ */

// ─────────────────────────────────────────────
//  FIGURE NAMES MAP
// ─────────────────────────────────────────────
const FIGURE_NAMES = {
  square: 'Quadrado',
  rectangle: 'Retângulo',
  triangle: 'Triângulo',
  equilateral_triangle: 'Triângulo Equilátero',
  trapezoid: 'Trapézio',
  rhombus: 'Losango',
  circle: 'Círculo',
  hexagon: 'Hexágono Regular',
};

// ─────────────────────────────────────────────
//  SVG FIGURE RENDERER
// ─────────────────────────────────────────────
function drawFigureSVG(type, w = 120, h = 120) {
  const ns = 'http://www.w3.org/2000/svg';
  const svg = document.createElementNS(ns, 'svg');
  svg.setAttribute('width', w);
  svg.setAttribute('height', h);
  svg.setAttribute('viewBox', `0 0 ${w} ${h}`);

  const pad = 14;
  const W = w - pad * 2;
  const H = h - pad * 2;
  const cx = w / 2, cy = h / 2;

  const mainFill = '#4895D9';
  const stroke   = '#173F73';
  const strokeW  = '2.5';

  function poly(pts) {
    const el = document.createElementNS(ns, 'polygon');
    el.setAttribute('points', pts.map(p => p.join(',')).join(' '));
    el.setAttribute('fill', mainFill);
    el.setAttribute('stroke', stroke);
    el.setAttribute('stroke-width', strokeW);
    el.setAttribute('stroke-linejoin', 'round');
    svg.appendChild(el);
  }

  function circ(r) {
    const el = document.createElementNS(ns, 'circle');
    el.setAttribute('cx', cx); el.setAttribute('cy', cy); el.setAttribute('r', r);
    el.setAttribute('fill', mainFill);
    el.setAttribute('stroke', stroke);
    el.setAttribute('stroke-width', strokeW);
    svg.appendChild(el);
  }

  switch (type) {
    case 'square': {
      const s = Math.min(W, H);
      const x0 = cx - s/2, y0 = cy - s/2;
      poly([[x0,y0],[x0+s,y0],[x0+s,y0+s],[x0,y0+s]]);
      break;
    }
    case 'rectangle': {
      const bw = W, bh = H * 0.6;
      poly([[cx-bw/2, cy-bh/2],[cx+bw/2, cy-bh/2],[cx+bw/2, cy+bh/2],[cx-bw/2, cy+bh/2]]);
      break;
    }
    case 'triangle': {
      poly([[cx, pad],[cx+W/2, h-pad],[cx-W/2, h-pad]]);
      break;
    }
    case 'equilateral_triangle': {
      const R = Math.min(W, H) / 2;
      const pts = [0,1,2].map(i => {
        const a = -Math.PI/2 + i * 2*Math.PI/3;
        return [cx + R*Math.cos(a), cy + R*Math.sin(a)];
      });
      poly(pts);
      break;
    }
    case 'trapezoid': {
      const bTop = W * 0.55, bBot = W;
      poly([
        [cx - bTop/2, pad],
        [cx + bTop/2, pad],
        [cx + bBot/2, h - pad],
        [cx - bBot/2, h - pad],
      ]);
      break;
    }
    case 'rhombus': {
      poly([[cx, pad],[cx+W/2, cy],[cx, h-pad],[cx-W/2, cy]]);
      break;
    }
    case 'circle': {
      circ(Math.min(W, H) / 2);
      break;
    }
    case 'hexagon': {
      const R = Math.min(W, H) / 2;
      const pts = Array.from({length:6}, (_,i) => {
        const a = -Math.PI/2 + i * Math.PI/3;
        return [cx + R*Math.cos(a), cy + R*Math.sin(a)];
      });
      poly(pts);
      break;
    }
    default: {
      const el = document.createElementNS(ns, 'text');
      el.setAttribute('x', cx); el.setAttribute('y', cy);
      el.setAttribute('text-anchor', 'middle');
      el.setAttribute('dominant-baseline', 'middle');
      el.setAttribute('font-size', '14');
      el.textContent = type;
      svg.appendChild(el);
    }
  }
  return svg;
}

// ─────────────────────────────────────────────
//  LESSON ENGINE  (only runs on lesson page)
// ─────────────────────────────────────────────
if (typeof LESSON_CONFIG !== 'undefined') {
  const { unitId, activityId } = LESSON_CONFIG;

  let questions = [];
  let currentIdx = 0;
  let answeredCorrect = 0;
  let xpEarned = 0;
  let answered = false;
  let timerInterval = null;

  // DOM refs
  const exerciseArea  = document.getElementById('exercise-area');
  const footer        = document.getElementById('lesson-footer');
  const btnCheck      = document.getElementById('btn-check');
  const feedbackBanner= document.getElementById('feedback-banner');
  const progressFill  = document.getElementById('progress-fill');
  const xpChip        = document.getElementById('xp-chip');
  const compScreen    = document.getElementById('completion-screen');

  // ── Bootstrap ──
  (async () => {
    const res = await fetch(`/api/questions/${unitId}/${activityId}`);
    questions = await res.json();
    if (!questions.length) {
      exerciseArea.innerHTML = '<p style="text-align:center;color:#7A8DB5">Sem questões disponíveis.</p>';
      return;
    }
    renderQuestion(0);
  })();

  // ── Progress bar ──
  function updateProgressBar() {
    const pct = (currentIdx / questions.length) * 100;
    progressFill.style.width = pct + '%';
  }

  // ── Render dispatcher ──
  function renderQuestion(idx) {
    answered = false;
    clearTimer();
    updateProgressBar();
    footer.style.display = 'flex';
    feedbackBanner.style.display = 'none';
    btnCheck.disabled = true;
    btnCheck.textContent = 'Verificar';

    const q = questions[idx];
    exerciseArea.innerHTML = '';

    const card = document.createElement('div');
    card.className = 'question-card';

    // Timer bar (timed questions)
    if (q.timed && q.time_limit) {
      const timerWrap = document.createElement('div');
      timerWrap.className = 'timer-bar-wrap';
      timerWrap.innerHTML = `
        <div class="timer-bar-track">
          <div class="timer-bar-fill" id="timer-fill" style="width:100%"></div>
        </div>
        <div class="timer-label" id="timer-label">${q.time_limit}s</div>`;
      card.appendChild(timerWrap);
      startTimer(q.time_limit);
    }

    // Question text
    const qText = document.createElement('div');
    qText.className = 'question-text';
    qText.textContent = q.question;
    card.appendChild(qText);

    // Figure display (if present and not null)
    if (q.figure) {
      const figWrap = document.createElement('div');
      figWrap.className = 'figure-display';
      figWrap.appendChild(drawFigureSVG(q.figure, 150, 150));
      card.appendChild(figWrap);
    }

    // Exercise body by type
    switch (q.type) {
      case 'multiple_choice':          renderMC(card, q);          break;
      case 'multiple_choice_figure':   renderMCFig(card, q);       break;
      case 'fill_blank':               renderFillBlank(card, q);   break;
      case 'drag_drop':                renderDragDrop(card, q);    break;
      case 'memory_match':             renderMemoryMatch(card, q); break;
      case 'order_steps':              renderOrderSteps(card, q);  break;
      default:                         renderMC(card, q);
    }

    exerciseArea.appendChild(card);
  }

  // ══════════════════════════════════════════════
  //  EXERCISE TYPES
  // ══════════════════════════════════════════════

  // ── Multiple Choice ──
  function renderMC(card, q) {
    const grid = document.createElement('div');
    grid.className = 'options-grid';

    q.options.forEach((opt, i) => {
      const btn = document.createElement('button');
      btn.className = 'option-btn';
      btn.textContent = opt;
      btn.dataset.idx = i;
      btn.addEventListener('click', () => {
        if (answered) return;
        grid.querySelectorAll('.option-btn').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        btnCheck.disabled = false;
        btnCheck.dataset.selected = i;
      });
      grid.appendChild(btn);
    });

    btnCheck.onclick = () => {
      if (answered) return;
      const sel = parseInt(btnCheck.dataset.selected);
      checkMC(grid, q, sel);
    };

    card.appendChild(grid);
  }

  function checkMC(grid, q, sel) {
    answered = true;
    clearTimer();
    const correct = sel === q.correct;
    const btns = grid.querySelectorAll('.option-btn');
    btns.forEach(b => b.disabled = true);
    btns[q.correct].classList.add('correct');
    if (!correct) btns[sel]?.classList.add('wrong');
    showFeedback(correct, q);
    submitAnswer(q, correct);
  }

  // ── Multiple Choice Figure ──
  function renderMCFig(card, q) {
    const grid = document.createElement('div');
    grid.className = 'figure-options-grid';

    q.options.forEach((fig, i) => {
      const btn = document.createElement('button');
      btn.className = 'fig-option-btn';
      btn.dataset.idx = i;
      btn.appendChild(drawFigureSVG(fig, 110, 90));
      // NO label — question asks to identify by shape only
      btn.addEventListener('click', () => {
        if (answered) return;
        grid.querySelectorAll('.fig-option-btn').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        btnCheck.disabled = false;
        btnCheck.dataset.selected = i;
      });
      grid.appendChild(btn);
    });

    btnCheck.onclick = () => {
      if (answered) return;
      const sel = parseInt(btnCheck.dataset.selected);
      answered = true;
      clearTimer();
      const correct = sel === q.correct;
      const btns = grid.querySelectorAll('.fig-option-btn');
      btns.forEach(b => b.disabled = true);
      btns[q.correct].classList.add('correct');
      if (!correct) btns[sel]?.classList.add('wrong');
      showFeedback(correct, q);
      submitAnswer(q, correct);
    };
    card.appendChild(grid);
  }

  // ── Fill Blank ──
  function renderFillBlank(card, q) {
    const area = document.createElement('div');
    area.className = 'fill-area';

    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'text-input';
    input.placeholder = 'Digite sua resposta...';
    input.addEventListener('input', () => { btnCheck.disabled = input.value.trim() === ''; });
    input.addEventListener('keydown', e => { if (e.key === 'Enter' && !btnCheck.disabled) checkFill(); });
    area.appendChild(input);

    // Hint button
    if (q.hint) {
      const hintBtn = document.createElement('button');
      hintBtn.className = 'hint-btn';
      hintBtn.textContent = '💡 Dica';
      const hintBox = document.createElement('div');
      hintBox.className = 'hint-box';
      hintBox.style.display = 'none';
      hintBox.textContent = q.hint;
      hintBtn.addEventListener('click', () => { hintBox.style.display = hintBox.style.display === 'none' ? 'block' : 'none'; });
      area.appendChild(hintBtn);
      area.appendChild(hintBox);
    }

    function checkFill() {
      if (answered) return;
      answered = true;
      clearTimer();
      const userVal = input.value.trim().replace(',', '.').replace(/\s/g, '');
      const correctVal = String(q.answer).replace(',', '.').replace(/\s/g, '');
      // Accept numeric near-equality (within 1% or 0.02 abs)
      let correct = false;
      const uNum = parseFloat(userVal), cNum = parseFloat(correctVal);
      if (!isNaN(uNum) && !isNaN(cNum)) {
        correct = Math.abs(uNum - cNum) <= Math.max(0.02, Math.abs(cNum) * 0.01);
      } else {
        correct = userVal.toLowerCase() === correctVal.toLowerCase() ||
                  userVal.toLowerCase() === q.answer.toString().toLowerCase();
      }
      input.disabled = true;
      input.classList.add(correct ? 'correct' : 'wrong');
      if (!correct) {
        const corrHint = document.createElement('div');
        corrHint.className = 'hint-box';
        corrHint.textContent = `✓ Resposta correta: ${q.answer}`;
        area.appendChild(corrHint);
      }
      showFeedback(correct, q);
      submitAnswer(q, correct);
    }

    btnCheck.onclick = checkFill;
    card.appendChild(area);
  }

  // ── Drag & Drop ──
  function renderDragDrop(card, q) {
    const area = document.createElement('div');
    area.className = 'drag-area';

    // Chips bank
    const bank = document.createElement('div');
    bank.className = 'drag-chips';
    bank.id = 'chip-bank';

    const shuffled = [...q.items].sort(() => Math.random() - .5);
    shuffled.forEach(item => bank.appendChild(createChip(item)));
    area.appendChild(bank);

    // Targets
    const targetsWrap = document.createElement('div');
    targetsWrap.className = 'drag-targets';

    q.targets.forEach(tgt => {
      const row = document.createElement('div');
      row.className = 'drag-target';
      row.id = 'target-' + tgt.id;
      row.dataset.correct = tgt.correct;

      // Figure or text label
      if (tgt.figure) {
        const fw = document.createElement('div');
        fw.className = 'target-figure';
        fw.appendChild(drawFigureSVG(tgt.figure, 70, 60));
        row.appendChild(fw);
      } else if (tgt.text) {
        const tl = document.createElement('div');
        tl.className = 'target-text-label';
        tl.textContent = tgt.text;
        row.appendChild(tl);
      }

      const zone = document.createElement('div');
      zone.className = 'target-drop-zone';
      zone.id = 'zone-' + tgt.id;
      row.appendChild(zone);
      targetsWrap.appendChild(row);

      // Drop events
      row.addEventListener('dragover', e => { e.preventDefault(); row.classList.add('drag-over'); });
      row.addEventListener('dragleave', () => row.classList.remove('drag-over'));
      row.addEventListener('drop', e => {
        e.preventDefault();
        row.classList.remove('drag-over');
        const chipText = e.dataTransfer.getData('text/plain');
        if (!chipText) return;
        // Return previous chip to bank
        const existing = zone.querySelector('.drag-chip');
        if (existing) bank.appendChild(existing);
        const newChip = createChip(chipText);
        zone.innerHTML = '';
        zone.appendChild(newChip);
        row.classList.add('has-chip');
        checkDragComplete(q, targetsWrap);
      });
      // Touch support
      row.addEventListener('touchend', handleTouchDrop);
    });

    area.appendChild(targetsWrap);

    btnCheck.onclick = () => {
      if (answered) return;
      gradeDragDrop(q, targetsWrap);
    };

    card.appendChild(area);
  }

  function createChip(text) {
    const chip = document.createElement('button');
    chip.className = 'drag-chip';
    chip.textContent = text;
    chip.draggable = true;
    chip.addEventListener('dragstart', e => {
      e.dataTransfer.setData('text/plain', text);
      chip.classList.add('dragging');
      setTimeout(() => { if (chip.parentNode) chip.style.opacity = '.4'; }, 0);
    });
    chip.addEventListener('dragend', () => {
      chip.classList.remove('dragging');
      chip.style.opacity = '1';
    });
    // Touch drag support
    chip.addEventListener('touchstart', handleTouchStart, { passive: true });
    chip.addEventListener('touchmove', handleTouchMove, { passive: false });
    chip.addEventListener('touchend', handleTouchEnd);
    return chip;
  }

  // Touch drag globals
  let touchDragging = null, touchClone = null;
  function handleTouchStart(e) {
    touchDragging = e.currentTarget;
    const rect = touchDragging.getBoundingClientRect();
    touchClone = touchDragging.cloneNode(true);
    touchClone.style.cssText = `position:fixed;z-index:9999;pointer-events:none;opacity:.8;
      width:${rect.width}px;top:${rect.top}px;left:${rect.left}px;`;
    document.body.appendChild(touchClone);
  }
  function handleTouchMove(e) {
    e.preventDefault();
    const t = e.touches[0];
    if (touchClone) {
      touchClone.style.top = (t.clientY - 20) + 'px';
      touchClone.style.left = (t.clientX - 40) + 'px';
    }
  }
  function handleTouchEnd(e) {
    if (touchClone) { touchClone.remove(); touchClone = null; }
    const t = e.changedTouches[0];
    const el = document.elementFromPoint(t.clientX, t.clientY);
    if (!el) return;
    const target = el.closest('.drag-target');
    if (target && touchDragging) {
      const zone = target.querySelector('.target-drop-zone');
      const bank = document.getElementById('chip-bank');
      const existing = zone.querySelector('.drag-chip');
      if (existing && bank) bank.appendChild(existing);
      zone.innerHTML = '';
      const newChip = createChip(touchDragging.textContent);
      zone.appendChild(newChip);
      target.classList.add('has-chip');
      // Return original to bank
      if (touchDragging.closest('.drag-target') === null && bank) {
        // already in bank, remove it
        touchDragging.remove();
      } else if (bank) {
        bank.appendChild(createChip(touchDragging.textContent));
        touchDragging.remove();
      }
    }
    touchDragging = null;
  }
  function handleTouchDrop() { /* handled by handleTouchEnd */ }

  function checkDragComplete(q, targetsWrap) {
    const zones = targetsWrap.querySelectorAll('.target-drop-zone');
    let allFilled = true;
    zones.forEach(z => { if (!z.querySelector('.drag-chip')) allFilled = false; });
    btnCheck.disabled = !allFilled;
  }

  function gradeDragDrop(q, targetsWrap) {
    answered = true;
    clearTimer();
    let allCorrect = true;
    q.targets.forEach(tgt => {
      const row = document.getElementById('target-' + tgt.id);
      const zone = document.getElementById('zone-' + tgt.id);
      const chip = zone?.querySelector('.drag-chip');
      const placed = chip ? chip.textContent.trim() : '';
      // Accept partial match (e.g. 'Losando' typo in data)
      const isCorrect = placed === tgt.correct ||
        placed.toLowerCase() === tgt.correct.toLowerCase() ||
        tgt.correct.toLowerCase().startsWith(placed.toLowerCase().slice(0,5));
      row?.classList.add(isCorrect ? 'correct' : 'wrong');
      if (!isCorrect) allCorrect = false;
    });
    showFeedback(allCorrect, q);
    submitAnswer(q, allCorrect);
  }

  // ── Memory Match ──
  function renderMemoryMatch(card, q) {
    // Build left (figures) and right (text) columns
    const pairs = q.pairs;
    const shuffledLeft  = [...pairs].sort(() => Math.random() - .5);
    const shuffledRight = [...pairs].sort(() => Math.random() - .5);

    const area = document.createElement('div');
    area.className = 'match-area';

    const leftCol  = document.createElement('div'); leftCol.className  = 'match-col';
    const rightCol = document.createElement('div'); rightCol.className = 'match-col';

    let selectedLeft = null, selectedRight = null, matchedCount = 0;

    shuffledLeft.forEach((pair, i) => {
      const card2 = document.createElement('div');
      card2.className = 'match-card';
      card2.dataset.pairIndex = i;
      card2.dataset.pairId = shuffledLeft.indexOf(pair);
      // Figure card
      if (pair.left.kind === 'figure') {
        card2.appendChild(drawFigureSVG(pair.left.value, 90, 70));
      } else {
        card2.textContent = pair.left.value;
      }
      card2.addEventListener('click', () => selectLeft(card2, pair, leftCol, rightCol));
      leftCol.appendChild(card2);
    });

    shuffledRight.forEach((pair, i) => {
      const card2 = document.createElement('div');
      card2.className = 'match-card';
      card2.dataset.pairIndex = i;
      card2.textContent = pair.right.value;
      card2.addEventListener('click', () => selectRight(card2, pair, leftCol, rightCol));
      rightCol.appendChild(card2);
    });

    function selectLeft(el, pair, lc, rc) {
      if (el.classList.contains('matched')) return;
      lc.querySelectorAll('.match-card:not(.matched)').forEach(c => c.classList.remove('selected'));
      el.classList.add('selected');
      selectedLeft = { el, pair };
      if (selectedRight) tryMatch(lc, rc);
    }

    function selectRight(el, pair, lc, rc) {
      if (el.classList.contains('matched')) return;
      rc.querySelectorAll('.match-card:not(.matched)').forEach(c => c.classList.remove('selected'));
      el.classList.add('selected');
      selectedRight = { el, pair };
      if (selectedLeft) tryMatch(lc, rc);
    }

    function tryMatch(lc, rc) {
      const lPair = selectedLeft.pair;
      const rPair = selectedRight.pair;
      const isMatch = lPair.left.value === rPair.left.value;
      if (isMatch) {
        selectedLeft.el.classList.remove('selected');
        selectedRight.el.classList.remove('selected');
        selectedLeft.el.classList.add('matched');
        selectedRight.el.classList.add('matched');
        matchedCount++;
        if (matchedCount === pairs.length) {
          btnCheck.disabled = false;
          btnCheck.dataset.matchResult = 'true';
        }
      } else {
        selectedLeft.el.classList.add('wrong-flash');
        selectedRight.el.classList.add('wrong-flash');
        setTimeout(() => {
          selectedLeft?.el.classList.remove('wrong-flash', 'selected');
          selectedRight?.el.classList.remove('wrong-flash', 'selected');
        }, 500);
      }
      selectedLeft = null; selectedRight = null;
    }

    btnCheck.onclick = () => {
      if (answered) return;
      answered = true;
      clearTimer();
      const allMatched = matchedCount === pairs.length;
      showFeedback(allMatched, q);
      submitAnswer(q, allMatched);
    };

    area.appendChild(leftCol);
    area.appendChild(rightCol);
    card.appendChild(area);
  }

  // ── Order Steps ──
  function renderOrderSteps(card, q) {
    const area = document.createElement('div');
    area.className = 'steps-list';

    // Shuffle the steps for display
    const display = [...q.steps].map((text, i) => ({ text, origIdx: i }))
      .sort(() => Math.random() - .5);

    let selectedOrder = [];

    display.forEach((step, dispIdx) => {
      const item = document.createElement('div');
      item.className = 'step-item';
      item.dataset.origIdx = step.origIdx;

      const num = document.createElement('div');
      num.className = 'step-number';
      num.textContent = '?';
      item.appendChild(num);

      const txt = document.createElement('div');
      txt.style.flex = '1';
      txt.textContent = step.text;
      item.appendChild(txt);

      item.addEventListener('click', () => {
        if (answered) return;
        if (item.classList.contains('selected')) {
          item.classList.remove('selected');
          num.textContent = '?';
          selectedOrder = selectedOrder.filter(o => o.origIdx !== step.origIdx);
          // Re-number remaining
          selectedOrder.forEach((o, rank) => {
            const el = area.querySelector(`[data-orig-idx="${o.origIdx}"] .step-number`);
            if (el) el.textContent = rank + 1;
          });
        } else {
          selectedOrder.push(step);
          item.classList.add('selected');
          num.textContent = selectedOrder.length;
        }
        btnCheck.disabled = selectedOrder.length !== q.steps.length;
      });

      area.appendChild(item);
    });

    btnCheck.onclick = () => {
      if (answered) return;
      answered = true;
      clearTimer();
      // Compare selectedOrder (by origIdx) with correct_order
      const userOrder = selectedOrder.map(o => o.origIdx);
      const correct = JSON.stringify(userOrder) === JSON.stringify(q.correct_order);

      area.querySelectorAll('.step-item').forEach(item => {
        const oi = parseInt(item.dataset.origIdx);
        const rank = userOrder.indexOf(oi);
        const correctRank = q.correct_order.indexOf(oi);
        if (rank === correctRank) item.classList.add('correct');
        else if (item.classList.contains('selected')) item.classList.add('wrong');
      });

      showFeedback(correct, q);
      submitAnswer(q, correct);
    };

    card.appendChild(area);
  }

  // ──────────────────────────────────────────────
  //  FEEDBACK & PROGRESSION
  // ──────────────────────────────────────────────
  function showFeedback(correct, q) {
    clearTimer();
    footer.style.display = 'none';
    feedbackBanner.style.display = 'flex';
    feedbackBanner.className = 'feedback-banner ' + (correct ? 'correct-fb' : 'wrong-fb');
    document.getElementById('fb-title').textContent = correct ? 'Correto!' : 'Ops! Não foi dessa vez.';
    document.getElementById('fb-exp').textContent = q.explanation || '';
    if (correct) {
      xpEarned += (q.xp || 10);
      answeredCorrect++;
      const xpEl = xpChip;
      if (xpEl) {
        const parts = xpEl.textContent.split(' ');
        const cur = parseInt(parts[1]) || 0;
        xpEl.textContent = `⚡ ${cur + (q.xp||10)} XP`;
        xpEl.style.animation = 'none';
        requestAnimationFrame(() => { xpEl.style.animation = 'pop-in .4s'; });
      }
    }
  }

  window.checkAnswer = function() {
    // Triggered by footer button – actual check is wired per-type
    btnCheck.click();
  };

  window.nextQuestion = function() {
    feedbackBanner.style.display = 'none';
    currentIdx++;
    if (currentIdx >= questions.length) {
      progressFill.style.width = '100%';
      setTimeout(showCompletion, 400);
    } else {
      renderQuestion(currentIdx);
    }
  };

  function showCompletion() {
    compScreen.style.display = 'flex';
    document.getElementById('comp-xp').textContent = xpEarned;
    document.getElementById('comp-correct').textContent = `${answeredCorrect}/${questions.length}`;
  }

  async function submitAnswer(q, correct) {
    await fetch('/api/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        unit_id: unitId,
        activity_id: activityId,
        question_id: q.id,
        correct,
        xp: correct ? (q.xp || 10) : 0,
      }),
    });
  }

  // ──────────────────────────────────────────────
  //  TIMER
  // ──────────────────────────────────────────────
  function startTimer(seconds) {
    let remaining = seconds;
    timerInterval = setInterval(() => {
      remaining--;
      const fill = document.getElementById('timer-fill');
      const label = document.getElementById('timer-label');
      if (!fill) { clearInterval(timerInterval); return; }
      fill.style.width = ((remaining / seconds) * 100) + '%';
      if (label) label.textContent = remaining + 's';
      if (remaining <= 5) fill.classList.add('urgent');
      if (remaining <= 0) {
        clearInterval(timerInterval);
        if (!answered) {
          answered = true;
          const q = questions[currentIdx];
          showFeedback(false, { ...q, explanation: '⏱️ Tempo esgotado! ' + (q.explanation||'') });
          submitAnswer(q, false);
        }
      }
    }, 1000);
  }

  function clearTimer() {
    if (timerInterval) { clearInterval(timerInterval); timerInterval = null; }
  }
}
