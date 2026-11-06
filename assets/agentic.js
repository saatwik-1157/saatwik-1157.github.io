/* The agent layer: a team of coloured cursors assembles the page in front of the
   visitor, then keeps working on whatever scrolls into view.

   Rules this file keeps:
   - The text in index.html is the page. Effects only hide it for a moment, then
     put back the exact original markup.
   - Any scroll, tap or key press ends the intro immediately.
   - prefers-reduced-motion turns all of it off; "Agents off" stops it on demand. */
(function () {
  'use strict';
  var root = document.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia('(pointer: fine)').matches;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };

  var canvas = $('#agents');
  var ctx = canvas && canvas.getContext('2d');
  var consoleEl = $('#console');
  if (reduce || !ctx) {
    if (canvas) canvas.hidden = true;
    if (consoleEl) consoleEl.hidden = true;
    root.classList.remove('building');
    return;
  }

  var COLORS = ['#7dd3fc', '#c4b5fd', '#f9a8d4', '#86efac', '#fde68a', '#fdba74', '#67e8f9', '#e9d5ff'];
  var NAMES = ['schema-agent', 'etl-agent', 'ml-agent', 'ui-agent', 'qa-agent', 'ci-agent', 'docs-agent', 'verify-agent'];
  var BLUE = '#2f9bff', RED = '#ff3b30', MONO = '"JetBrains Mono", Consolas, monospace';
  var GLYPHS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/#$%&*+<>';
  var ARROW = new Path2D('M0 0 L0 15.5 L4.3 11.6 L7.4 18.4 L10.2 17.1 L7.1 10.5 L12.6 10.3 Z');

  var W = 0, H = 0, DPR = 1, guideX = 40;
  var agentsOn = true, building = false, swarm = false, crossPhase = false;
  var agents = [], boxes = [], sparks = [], rings = [], tasks = [], timers = [];
  var pointer = null, pointerMoved = false, contactVisible = false, footVisible = false;
  var last = performance.now(), rafId = 0, rulerA = 0, swarmStart = 0;

  function resize() {
    DPR = Math.min(window.devicePixelRatio || 1, 2);
    W = window.innerWidth;
    H = window.innerHeight;
    canvas.width = Math.round(W * DPR);
    canvas.height = Math.round(H * DPR);
    var wrap = $('.sec .wrap');
    if (wrap) guideX = wrap.getBoundingClientRect().left + parseFloat(getComputedStyle(wrap).paddingLeft) - 11;
  }
  resize();
  window.addEventListener('resize', resize);

  var count = W < 720 ? 9 : 18;
  for (var n = 0; n < count; n++) {
    agents.push({
      x: W / 2 + (Math.random() - .5) * 240, y: H / 2 + (Math.random() - .5) * 240,
      vx: 0, vy: 0, tx: W / 2, ty: H / 2, nextWander: 0, i: n,
      color: COLORS[n % COLORS.length], name: NAMES[n % NAMES.length],
      job: false, mode: 'arrow', pop: 0,
      orbitR: 46 + Math.random() * 170, orbitA: Math.random() * Math.PI * 2, orbitS: .9 + Math.random() * 1.4
    });
  }

  function grab(x, y, mode) {
    var best = null, bestD = Infinity;
    agents.forEach(function (a) {
      if (a.job) return;
      var d = (a.x - x) * (a.x - x) + (a.y - y) * (a.y - y);
      if (d < bestD) { bestD = d; best = a; }
    });
    if (best) { best.job = true; best.mode = mode; best.pop = 1; }
    return best;
  }
  function release(a) {
    if (!a) return;
    a.job = false;
    a.mode = crossPhase ? 'cross' : 'arrow';
    a.pop = 1;
    a.nextWander = 0;
  }

  function spark(x, y, color, many) {
    for (var k = 0; k < (many || 5); k++) {
      var a = Math.random() * Math.PI * 2, s = 30 + Math.random() * (many ? 240 : 70);
      sparks.push({ x: x, y: y, vx: Math.cos(a) * s, vy: Math.sin(a) * s, life: .6, color: color });
    }
  }
  function ring(x, y, color, max) { rings.push({ x: x, y: y, color: color || RED, r: 4, max: max || 90, life: 1 }); }

  /* ---------- Selection boxes ---------- */
  function addBox(el, opts) {
    opts = opts || {};
    var r = el.getBoundingClientRect();
    if (!r.width || !r.height) return null;
    var box = {
      el: el, start: performance.now() + (opts.delay || 0), draw: opts.draw || 380, hold: opts.hold || 520,
      fade: 320, ghost: !!opts.ghost, color: opts.color || BLUE, inset: opts.inset || 0, guides: !!opts.guides,
      onDone: opts.onDone || null, done: false, agent: null
    };
    boxes.push(box);
    return box;
  }

  function sizeLabel(cx, y, text, color) {
    ctx.font = '700 10px ' + MONO;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    var tw = ctx.measureText(text).width + 10;
    ctx.fillStyle = color;
    ctx.fillRect(cx - tw / 2, y, tw, 15);
    ctx.fillStyle = '#fff';
    ctx.fillText(text, cx, y + 8);
  }

  function drawBox(box, now) {
    var t = now - box.start;
    if (t < 0) return true;
    var o = box.el.getBoundingClientRect();
    var r = { left: o.left + box.inset, top: o.top + box.inset, width: Math.max(0, o.width - box.inset * 2), height: Math.max(0, o.height - box.inset * 2) };
    var total = box.draw + box.hold + box.fade;
    if (!box.agent) box.agent = grab(r.left, r.top, 'cross');
    var p = Math.min(1, t / box.draw);
    p = 1 - Math.pow(1 - p, 3);
    var w = r.width * p, h = r.height * p;
    if (box.agent) { box.agent.tx = r.left + w; box.agent.ty = r.top + h; }
    if (t >= box.draw + box.hold && !box.done) {
      box.done = true;
      if (box.agent) { spark(r.left + w, r.top + h, box.agent.color); release(box.agent); box.agent = null; }
      if (box.onDone) box.onDone();
    }
    if (t >= total) return false;
    if (o.bottom < -40 || o.top > H + 40) return true;
    var alpha = t > box.draw + box.hold ? 1 - (t - box.draw - box.hold) / box.fade : 1;

    /* Smart guides reach out across the canvas while the box is being drawn. */
    if (box.guides && t < box.draw + box.hold) {
      ctx.globalAlpha = .4 * alpha;
      ctx.strokeStyle = '#ff5cf0';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(r.left + .5, 0); ctx.lineTo(r.left + .5, H);
      ctx.moveTo(0, r.top + .5); ctx.lineTo(W, r.top + .5);
      ctx.moveTo(r.left + w + .5, 0); ctx.lineTo(r.left + w + .5, H);
      ctx.stroke();
    }
    ctx.globalAlpha = alpha;
    if (box.ghost) { ctx.fillStyle = 'rgba(255,255,255,.075)'; ctx.fillRect(r.left, r.top, w, h); }
    ctx.strokeStyle = box.color;
    ctx.lineWidth = 1.25;
    ctx.strokeRect(r.left + .5, r.top + .5, w, h);
    ctx.fillStyle = '#fff';
    [[0, 0], [w, 0], [0, h], [w, h]].forEach(function (c) {
      ctx.fillRect(r.left + c[0] - 2.5, r.top + c[1] - 2.5, 5, 5);
      ctx.strokeRect(r.left + c[0] - 2.5, r.top + c[1] - 2.5, 5, 5);
    });
    if (w > 46 && h > 8) sizeLabel(r.left + w / 2, r.top + h + 6, Math.round(w) + ' × ' + Math.round(h), box.color);
    ctx.globalAlpha = 1;
    return true;
  }

  /* ---------- Tasks: anything that animates over time and can be finished early ---------- */
  function addTask(task) { tasks.push(task); return task; }
  function completeAll() { tasks.splice(0).forEach(function (t) { t.finish(); }); }

  function splitChars(el) {
    el._orig = el.innerHTML;
    var chars = [], nodes = [];
    var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(function (node) {
      if (!node.nodeValue.trim()) return;
      /* One wrapper per text node, so a flex parent still sees a single item. */
      var wrap = document.createElement('span');
      wrap.className = 'chw';
      Array.from(node.nodeValue.replace(/\s+/g, ' ')).forEach(function (c) {
        var s = document.createElement('span');
        s.className = c === ' ' ? 'ch on' : 'ch';
        s.textContent = c;
        wrap.appendChild(s);
        if (c !== ' ') chars.push(s);
      });
      node.parentNode.replaceChild(wrap, node);
    });
    return chars;
  }
  function restoreChars(el) {
    if (el._orig == null) return;
    el.innerHTML = el._orig;
    el._orig = null;
  }

  /* Types an element in with an I-beam agent at the caret, optionally inside a
     selection outline, then sweeps a text selection across it. */
  function typeFx(el, opts) {
    opts = opts || {};
    if (el._orig != null) return null;
    var chars = splitChars(el);
    if (!chars.length) { restoreChars(el); return null; }
    var dur = opts.dur || 600, selDur = opts.select ? 340 : 0, hold = opts.select ? 190 : 0;
    var t0 = performance.now() + (opts.delay || 0), shown = 0, marked = 0, agent = null, finished = false;
    var task = addTask({
      step: function (now) {
        var t = now - t0;
        if (t < 0) return true;
        if (!agent && opts.agent !== false) agent = grab(chars[0].getBoundingClientRect().left, chars[0].getBoundingClientRect().top, 'ibeam');
        var want = Math.ceil(clamp(t / dur, 0, 1) * chars.length);
        while (shown < want) chars[shown++].classList.add('on');
        var c = chars[Math.max(0, shown - 1)].getBoundingClientRect();
        if (agent) { agent.tx = c.right; agent.ty = c.top + 1; }
        if (opts.box) {
          var r = el.getBoundingClientRect();
          ctx.strokeStyle = BLUE;
          ctx.lineWidth = 1.25;
          ctx.strokeRect(r.left - 4.5, r.top - 2.5, r.width + 9, r.height + 5);
          sizeLabel(r.left + r.width / 2, r.bottom + 6, Math.round(r.width) + ' × ' + Math.round(r.height), BLUE);
        }
        if (t > dur && selDur) {
          var k = Math.ceil(clamp((t - dur) / selDur, 0, 1) * chars.length);
          while (marked < k) chars[marked++].classList.add('sel');
        }
        if (t >= dur + selDur + hold) { task.finish(); return false; }
        return true;
      },
      finish: function () {
        if (finished) return;
        finished = true;
        restoreChars(el);
        release(agent);
        agent = null;
        var at = tasks.indexOf(task);
        if (at >= 0) tasks.splice(at, 1);
        if (opts.onDone) opts.onDone();
      }
    });
    return task;
  }

  /* Decodes text from noise. Only for plain-text monospace elements, where every
     glyph has the same width, so the layout cannot jump. */
  function scramble(el, dur) {
    if (el.children.length || el._scr) return;
    var text = el.textContent, t0 = performance.now(), finished = false;
    dur = dur || 560;
    el._scr = true;
    var task = addTask({
      step: function (now) {
        var p = clamp((now - t0) / dur, 0, 1), done = Math.floor(p * text.length), out = text.slice(0, done);
        for (var i = done; i < text.length; i++) {
          var ch = text.charAt(i);
          out += /\s/.test(ch) ? ch : GLYPHS.charAt(Math.floor(Math.random() * GLYPHS.length));
        }
        el.textContent = out;
        if (p >= 1) { task.finish(); return false; }
        return true;
      },
      finish: function () {
        if (finished) return;
        finished = true;
        el.textContent = text;
        el._scr = false;
        var at = tasks.indexOf(task);
        if (at >= 0) tasks.splice(at, 1);
      }
    });
  }

  function countUp(el, dur) {
    if (el._cnt || el.children.length) return;
    var text = el.textContent, m = /^(\D*)([\d,]*\.?\d+)(.*)$/.exec(text);
    if (!m) return;
    var value = parseFloat(m[2].replace(/,/g, ''));
    /* A year is a label, not a measurement: decode it instead of counting up to it. */
    if (!m[1] && !m[3] && value >= 1900 && value < 2100 && m[2].indexOf('.') < 0) { scramble(el, dur || 900); return; }
    var dot = m[2].indexOf('.'), decimals = dot < 0 ? 0 : m[2].length - dot - 1, commas = m[2].indexOf(',') >= 0;
    var t0 = performance.now(), finished = false;
    dur = dur || 1100;
    el._cnt = true;
    el.classList.add('counting');
    var task = addTask({
      step: function (now) {
        var p = clamp((now - t0) / dur, 0, 1), eased = 1 - Math.pow(1 - p, 4), v = (value * eased).toFixed(decimals);
        if (commas) v = Number(v).toLocaleString('en-US');
        el.textContent = m[1] + v + m[3];
        if (p >= 1) { task.finish(); return false; }
        return true;
      },
      finish: function () {
        if (finished) return;
        finished = true;
        el.textContent = text;
        el._cnt = false;
        el.classList.remove('counting');
        var at = tasks.indexOf(task);
        if (at >= 0) tasks.splice(at, 1);
      }
    });
  }

  /* The portrait comes together from randomly dropped blocks that get finer. */
  function mosaicFx(photo, dur) {
    var img = $('img', photo);
    var finished = false;
    var cv = document.createElement('canvas');
    cv.className = 'mosaic';
    cv.setAttribute('aria-hidden', 'true');
    var r = photo.getBoundingClientRect();
    if (!img || !img.complete || !img.naturalWidth || !r.width) return;
    cv.width = Math.round(r.width);
    cv.height = Math.round(r.height);
    photo.appendChild(cv);
    var c = cv.getContext('2d');
    var small = document.createElement('canvas');
    var sc = small.getContext('2d');
    var STEPS = [30, 22, 15, 10, 6, 3], t0 = performance.now(), lastDraw = 0;
    var scale = Math.max(cv.width / img.naturalWidth, cv.height / img.naturalHeight);
    var dw = img.naturalWidth * scale, dh = img.naturalHeight * scale, dx = (cv.width - dw) / 2;
    var task = addTask({
      step: function (now) {
        var p = clamp((now - t0) / dur, 0, 1);
        if (now - lastDraw > 58) {
          lastDraw = now;
          var s = STEPS[Math.min(STEPS.length - 1, Math.floor(p * STEPS.length))];
          var cols = Math.ceil(cv.width / s), rows = Math.ceil(cv.height / s);
          small.width = cols;
          small.height = rows;
          sc.drawImage(img, dx / s, 0, dw / s, dh / s);
          c.clearRect(0, 0, cv.width, cv.height);
          c.imageSmoothingEnabled = false;
          var keep = .32 + p * .78;
          for (var y = 0; y < rows; y++) {
            for (var x = 0; x < cols; x++) {
              if (Math.random() < keep) c.drawImage(small, x, y, 1, 1, x * s, y * s, s, s);
            }
          }
        }
        if (p >= 1) { task.finish(); return false; }
        return true;
      },
      finish: function () {
        if (finished) return;
        finished = true;
        cv.remove();
        var at = tasks.indexOf(task);
        if (at >= 0) tasks.splice(at, 1);
      }
    });
  }

  /* ---------- Rulers and the red guide, shown once the visitor is reading ---------- */
  function drawRulers(dt) {
    var want = !building && W >= 900 && window.scrollY > H * .55;
    root.classList.toggle('rulers', want);
    rulerA += ((want ? 1 : 0) - rulerA) * Math.min(1, dt * 7);
    if (rulerA < .01) return;
    var S = 16, off = window.scrollY, v, y;
    ctx.globalAlpha = rulerA;
    ctx.fillStyle = 'rgba(16,11,12,.94)';
    ctx.fillRect(0, 0, W, S);
    ctx.fillRect(0, 0, S, H);
    ctx.strokeStyle = 'rgba(255,235,230,.3)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    for (v = 0; v < W; v += 10) {
      var hx = v % 100 === 0 ? S : v % 50 === 0 ? 8 : 4;
      ctx.moveTo(v + .5, S); ctx.lineTo(v + .5, S - hx);
    }
    for (v = Math.floor(off / 10) * 10; v < off + H; v += 10) {
      y = Math.round(v - off) + .5;
      var hy = v % 100 === 0 ? S : v % 50 === 0 ? 8 : 4;
      ctx.moveTo(S, y); ctx.lineTo(S - hy, y);
    }
    ctx.stroke();
    ctx.fillStyle = 'rgba(255,235,230,.62)';
    ctx.font = '500 8px ' + MONO;
    ctx.textAlign = 'left';
    ctx.textBaseline = 'top';
    for (v = 100; v < W; v += 100) ctx.fillText(String(v), v + 3, 1);
    ctx.save();
    ctx.rotate(-Math.PI / 2);
    for (v = Math.ceil(off / 100) * 100; v < off + H; v += 100) ctx.fillText(String(v), -(v - off) + 3, 1);
    ctx.restore();

    /* The reel's red vertical guide on the content edge. */
    ctx.globalAlpha = rulerA * .75;
    ctx.fillStyle = RED;
    ctx.fillRect(Math.round(guideX), S, 1, H - S);
    ctx.globalAlpha = rulerA;
    ctx.fillRect(Math.round(guideX) - 2, 0, 5, S);
    if (pointer) {
      ctx.fillStyle = BLUE;
      ctx.fillRect(pointer.x, 0, 1, S);
      ctx.fillRect(0, pointer.y, S, 1);
    }
    ctx.globalAlpha = 1;
  }

  function tag(x, y, text, color) {
    ctx.font = '700 9.5px ' + MONO;
    ctx.textAlign = 'left';
    ctx.textBaseline = 'middle';
    var tw = ctx.measureText(text).width + 10;
    ctx.fillStyle = color;
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(x, y, tw, 15, 4); else ctx.rect(x, y, tw, 15);
    ctx.fill();
    ctx.fillStyle = '#0b0708';
    ctx.fillText(text, x + 5, y + 8);
  }

  /* ---------- Frame ---------- */
  function frame(now) {
    rafId = requestAnimationFrame(frame);
    var dt = Math.min(.05, (now - last) / 1000);
    last = now;
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    ctx.clearRect(0, 0, W, H);

    drawRulers(dt);
    boxes = boxes.filter(function (b) { return drawBox(b, now); });
    tasks.slice().forEach(function (t) { t.step(now); });

    rings = rings.filter(function (g) {
      g.life -= dt * 1.7;
      if (g.life <= 0) return false;
      g.r += (g.max - g.r) * Math.min(1, dt * 7);
      ctx.globalAlpha = g.life * .8;
      ctx.strokeStyle = g.color;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(g.x, g.y, g.r, 0, Math.PI * 2);
      ctx.stroke();
      ctx.globalAlpha = 1;
      return true;
    });

    sparks = sparks.filter(function (s) {
      s.life -= dt;
      if (s.life <= 0) return false;
      s.x += s.vx * dt;
      s.y += s.vy * dt;
      ctx.strokeStyle = s.color;
      ctx.globalAlpha = Math.min(1, s.life * 2);
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(s.x - 4, s.y); ctx.lineTo(s.x + 4, s.y);
      ctx.moveTo(s.x, s.y - 4); ctx.lineTo(s.x, s.y + 4);
      ctx.stroke();
      ctx.globalAlpha = 1;
      return true;
    });

    var clock = (now - swarmStart) / 1000;
    agents.forEach(function (a) {
      if (!a.job) {
        if (swarm) {
          var ang = a.orbitA + clock * a.orbitS;
          a.tx = W / 2 + Math.cos(ang) * a.orbitR;
          a.ty = H / 2 + Math.sin(ang) * a.orbitR * .72;
        } else if (contactVisible && pointer) {
          /* Over the contact section the agents flock round the visitor's pointer. */
          var fa = -2.5 + a.i * .62, rad = 74 + (a.i % 3) * 16;
          a.tx = pointer.x + Math.cos(fa) * rad;
          a.ty = pointer.y + Math.sin(fa) * rad;
        } else if (footVisible) {
          /* The reel ends with the team parked in a corner: so does this page. */
          a.tx = W - 70 - (a.i % 6) * 22 + Math.sin(clock + a.i) * 7;
          a.ty = H - 88 - (a.i % 3) * 26 + Math.cos(clock * 1.3 + a.i) * 7;
        } else if (now > a.nextWander) {
          a.tx = 30 + Math.random() * (W - 60);
          a.ty = 70 + Math.random() * (H - 110);
          a.nextWander = now + 1200 + Math.random() * 2600;
        }
      }
      var k = a.job ? 150 : swarm ? 60 : 9, d = a.job ? 22 : swarm ? 12 : 5;
      a.vx += (k * (a.tx - a.x) - d * a.vx) * dt;
      a.vy += (k * (a.ty - a.y) - d * a.vy) * dt;
      a.x += a.vx * dt;
      a.y += a.vy * dt;

      var speed = Math.sqrt(a.vx * a.vx + a.vy * a.vy);
      if (speed > 260) {
        ctx.strokeStyle = a.color;
        ctx.globalAlpha = Math.min(.45, speed / 1800);
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.lineTo(a.x - a.vx * .045, a.y - a.vy * .045);
        ctx.stroke();
        ctx.globalAlpha = 1;
      }

      a.pop = Math.max(0, a.pop - dt * 5);
      ctx.save();
      ctx.translate(a.x, a.y);
      var pop = 1 + a.pop * .6;
      ctx.scale(pop, pop);
      if (a.mode === 'cross') {
        ctx.strokeStyle = 'rgba(10,6,8,.8)';
        ctx.lineWidth = 3.4;
        ctx.beginPath();
        ctx.moveTo(-7, 0); ctx.lineTo(7, 0); ctx.moveTo(0, -7); ctx.lineTo(0, 7);
        ctx.stroke();
        ctx.strokeStyle = a.color;
        ctx.lineWidth = 1.7;
        ctx.stroke();
      } else if (a.mode === 'ibeam') {
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 1.6;
        ctx.beginPath();
        ctx.moveTo(-3, 0); ctx.lineTo(3, 0);
        ctx.moveTo(0, 0); ctx.lineTo(0, 17);
        ctx.moveTo(-3, 17); ctx.lineTo(3, 17);
        ctx.stroke();
      } else {
        ctx.fillStyle = a.color;
        ctx.strokeStyle = 'rgba(10,6,8,.75)';
        ctx.lineWidth = 1;
        ctx.fill(ARROW);
        ctx.stroke(ARROW);
      }
      ctx.restore();
      if (a.job && W >= 720 && !building) tag(a.x + 12, a.y + 18, a.name, a.color);
    });

    if (pointer && !building) tag(pointer.x + 15, pointer.y + 20, 'you', RED);
    if (pointerMoved) { pointerMoved = false; onPointerFrame(); }
  }

  function start() {
    if (rafId) return;
    last = performance.now();
    rafId = requestAnimationFrame(frame);
  }
  function stop() {
    cancelAnimationFrame(rafId);
    rafId = 0;
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  }
  document.addEventListener('visibilitychange', function () {
    if (document.hidden) { finishBuild(); stop(); } else if (agentsOn) { start(); }
  });

  /* ---------- PORTFOLIO word: letters react to the pointer ---------- */
  var word = $('.word');
  var letters = [];
  if (word) {
    var plain = word.textContent;
    word.textContent = '';
    Array.from(plain).forEach(function (c) {
      var s = document.createElement('span');
      s.className = 'ltr';
      s.textContent = c;
      word.appendChild(s);
      letters.push(s);
    });
  }
  function onPointerFrame() {
    if (!pointer) return;
    root.style.setProperty('--gx', pointer.x + 'px');
    root.style.setProperty('--gy', pointer.y + 'px');
    if (window.scrollY > H) return;
    letters.forEach(function (s) {
      var r = s.getBoundingClientRect();
      var d = Math.hypot(pointer.x - (r.left + r.width / 2), pointer.y - (r.top + r.height / 2));
      var f = clamp(1 - d / 300, 0, 1);
      s.style.color = f > 0 ? 'rgba(255,59,48,' + (.1 + f * .75).toFixed(3) + ')' : '';
      s.style.translate = f > 0 ? '0 ' + (-f * 9).toFixed(1) + 'px' : '';
    });
  }

  /* ---------- Intro: the reel's sequence, beat by beat ---------- */
  var parts = $$('[data-b]');
  var photoWrap = $('.photo-wrap'), photo = $('.photo');
  var chip = null;
  function at(ms, fn) { timers.push(setTimeout(fn, ms)); }
  function built(el) { if (el) el.classList.add('built'); }

  function finishBuild() {
    if (!building) return;
    building = false;
    swarm = false;
    crossPhase = false;
    timers.forEach(clearTimeout);
    timers = [];
    completeAll();
    boxes = [];
    agents.forEach(function (a) { a.job = false; a.mode = 'arrow'; a.nextWander = 0; });
    if (chip) { chip.remove(); chip = null; }
    root.classList.remove('building', 'wire');
    parts.forEach(function (p) { p.classList.remove('built', 'empty'); });
    if (photoWrap) photoWrap.classList.remove('pb', 'pb-red', 'pb-badge');
    if (word) { word.classList.remove('neon'); word.classList.add('buzz'); }
  }

  function runBuild() {
    building = true;
    swarm = true;
    crossPhase = false;
    swarmStart = performance.now();
    timers.forEach(clearTimeout);
    timers = [];
    completeAll();
    boxes = [];
    parts.forEach(function (p) { p.classList.remove('built', 'empty'); });
    root.classList.remove('wire');
    root.classList.add('building');
    if (photoWrap) { photoWrap.classList.remove('pb-red', 'pb-badge'); photoWrap.classList.add('pb'); }
    if (word) word.classList.remove('neon', 'buzz');
    agents.forEach(function (a) { a.job = false; a.mode = 'arrow'; });
    start();

    var q = function (s) { return $(s); };
    var nav = q('.nav'), hello = q('.hello'), name = q('.name'), role = q('.role-tag'), lede = q('.lede');
    var link = q('.link-cta'), btn = q('.cta .btn'), stats = q('.stats'), sideChips = q('.side > .chips');
    var sides = $$('.side-item');

    /* Beat 1, 0 ms: black screen, logo in the middle, the team circling it. */
    if (chip) chip.remove();
    chip = document.createElement('div');
    chip.className = 'intro-chip';
    chip.setAttribute('aria-hidden', 'true');
    chip.textContent = 'SV';
    document.body.appendChild(chip);

    /* Beat 2, 950 ms: arrows turn into crosshairs and burst outwards; the logo flies to the nav. */
    at(950, function () {
      swarm = false;
      crossPhase = true;
      ring(W / 2, H / 2, RED, Math.max(W, H) * .4);
      ring(W / 2, H / 2, '#fff', Math.max(W, H) * .22);
      spark(W / 2, H / 2, '#fff', 26);
      agents.forEach(function (a) {
        a.mode = 'cross';
        a.pop = 1;
        var ang = Math.atan2(a.y - H / 2, a.x - W / 2);
        a.vx += Math.cos(ang) * 1300;
        a.vy += Math.sin(ang) * 1300;
        a.tx = 30 + Math.random() * (W - 60);
        a.ty = 40 + Math.random() * (H - 80);
        a.nextWander = performance.now() + 900;
      });
      var brand = $('.brand i');
      if (chip && brand) {
        var b = brand.getBoundingClientRect();
        var sc = b.width / 56;
        chip.style.animation = 'none';
        chip.style.transform = 'translate(' + (b.left + b.width / 2 - W / 2) + 'px,' + (b.top + b.height / 2 - H / 2) + 'px) scale(' + sc + ')';
        chip.style.opacity = '0';
      }
    });

    /* Beat 3, 1250 ms: the page turns grey and is laid out as a wireframe. */
    at(1250, function () {
      root.classList.add('wire');
      built(word);
      built(nav);
      if (nav) {
        addBox(nav, { draw: 260, hold: 130, ghost: true });
        addBox($('.nav-links', nav), { delay: 120, draw: 220, hold: 150 });
        addBox($('.nav-end', nav), { delay: 200, draw: 220, hold: 150 });
      }
      if (word) addBox(word, { draw: 880, hold: 170, guides: true });
    });
    at(1350, function () { built(hello); if (hello) typeFx(hello, { dur: 320 }); });
    at(1480, function () {
      if (photoWrap) { built(photoWrap); addBox(photoWrap, { draw: 420, hold: 500, ghost: true, guides: true }); }
      if (name) { name.classList.add('empty'); built(name); addBox(name, { draw: 240, hold: 90 }); }
    });
    at(1680, function () {
      if (name) { name.classList.remove('empty'); typeFx(name, { dur: 310 }); }
      if (role) { built(role); typeFx(role, { dur: 430, select: true, box: true }); }
    });
    at(1760, function () { if (lede) { built(lede); typeFx(lede, { dur: 800, box: true }); } });
    at(1900, function () { if (photo) addBox(photo, { inset: 34, draw: 380, hold: 300 }); });
    sides.forEach(function (s, i) {
      at(1800 + i * 210, function () { built(s); typeFx(s, { dur: 470 }); addBox(s, { draw: 260, hold: 280 }); });
    });
    at(2130, function () {
      if (link) { built(link); typeFx(link, { dur: 240 }); }
      if (btn) { built(btn); addBox(btn, { draw: 200, hold: 180, ghost: true }); }
    });
    at(2400, function () {
      if (sideChips) { built(sideChips); popChips(sideChips); }
      if (stats) { built(stats); $$('b', stats).forEach(function (b) { countUp(b, 1500); }); addBox(stats, { draw: 240, hold: 240 }); }
    });

    /* Beat 4, 2650 ms: the wireframe flips to black and the crosshairs become arrows. */
    at(2650, function () {
      root.classList.remove('wire');
      crossPhase = false;
      agents.forEach(function (a) { if (!a.job) { a.mode = 'arrow'; a.pop = 1; } });
    });

    /* Beat 5, 2750 ms: the portrait assembles; the side panel gets its red selections. */
    at(2750, function () {
      if (photo) mosaicFx(photo, 1050);
      sides.forEach(function (s, i) { addBox(s, { delay: i * 170, draw: 240, hold: 420, color: RED }); });
    });
    at(3650, function () {
      if (photoWrap) { photoWrap.classList.add('pb-red'); addBox(photoWrap, { draw: 320, hold: 260, color: RED }); }
      if (word) { word.classList.add('neon'); }
    });
    at(3950, function () {
      if (photoWrap) { photoWrap.classList.add('pb-badge'); photoWrap.classList.remove('pb'); photoWrap.classList.add('pb-red'); }
    });

    at(4750, finishBuild);
    /* Hard stop in case a timer or frame was starved. */
    at(8000, finishBuild);
  }

  /* Any real intent to read the page ends the sequence at once. */
  ['wheel', 'touchstart', 'keydown', 'pointerdown'].forEach(function (ev) {
    window.addEventListener(ev, finishBuild, { passive: true });
  });

  /* ---------- Scroll reveals ---------- */
  function popChips(group) {
    group.classList.remove('fx-pre');
    Array.prototype.forEach.call(group.children, function (c, i) {
      c.style.setProperty('--d', Math.min(i, 14) * 34 + 'ms');
      flash(c, 'fx-pop', 1300);
    });
  }
  function flash(el, cls, ms) {
    el.classList.add(cls);
    setTimeout(function () { el.classList.remove(cls); }, ms);
  }

  var RULES = [
    { sel: '.index', run: function (el) { typeFx(el, { dur: 460 }); } },
    { sel: '.sec-head .eyebrow, .stack-head, .sub-title', run: function (el) { scramble(el, 620); } },
    { sel: '.sec-title, .contact h2', run: function (el) { typeFx(el, { dur: 640, box: true, select: true }); } },
    { sel: '.sec-sub, .core-desc, .story > p:not(.quote), .contact-inner > p, .work > p, .job p', run: function (el) { flash(el, 'fx-wipe', 1000); } },
    { sel: '.quote', run: function (el) { typeFx(el, { dur: 950, select: true }); } },
    { sel: '.skill-row dt', run: function (el) { flash(el, 'fx-rise', 800); } },
    { sel: '.skill-row .chips, .sec .card .chips, .socials, .mail-row', run: popChips },
    { sel: '.filters', run: popChips },
    { sel: '.edu > div, .tile', stagger: 90, run: function (el) { flash(el, 'fx-rise', 1100); var b = $('b', el); if (b) countUp(b); } },
    { sel: '.job', stagger: 120, run: function (el) { flash(el, 'fx-job', 1200); } },
    { sel: '.cred', stagger: 55, run: function (el) { flash(el, 'fx-slide', 1200); } },
    { sel: '.card', run: function (el) {
      flash(el, 'fx-card', 800);
      if (boxes.length < 5) addBox(el, { draw: 500, hold: 340, guides: true });
    } }
  ];

  var armed = [];
  var revealIO = 'IntersectionObserver' in window ? new IntersectionObserver(function (entries) {
    entries.forEach(function (en) { if (en.isIntersecting) revealItem(en.target); });
  }, { threshold: .08, rootMargin: '0px 0px -5% 0px' }) : null;

  function revealItem(el, instant) {
    var item = el._fx;
    if (!item) return;
    el._fx = null;
    armed = armed.filter(function (x) { return x !== el; });
    if (revealIO) revealIO.unobserve(el);
    el.classList.remove('fx-pre');
    if (instant || !agentsOn) return;
    if (item.delay) el.style.setProperty('--d', item.delay + 'ms');
    item.run(el);
  }

  function armAll() {
    if (!revealIO) return;
    var groupCount = typeof WeakMap === 'function' ? new WeakMap() : null;
    RULES.forEach(function (rule) {
      $$(rule.sel).forEach(function (el) {
        if (el.closest('.hero') || el._fx) return;
        var delay = 0;
        if (rule.stagger && groupCount && el.parentNode) {
          var c = groupCount.get(el.parentNode) || 0;
          groupCount.set(el.parentNode, c + 1);
          delay = Math.min(c, 10) * rule.stagger;
        }
        el._fx = { run: rule.run, delay: delay };
        el.classList.add('fx-pre');
        armed.push(el);
        revealIO.observe(el);
      });
    });
  }
  function flushReveals() { armed.slice().forEach(function (el) { revealItem(el, true); }); }

  /* Selection boxes for the larger blocks that have no reveal of their own. */
  var queue = [], jobSeen = typeof WeakSet === 'function' ? new WeakSet() : null;
  if (revealIO && jobSeen) {
    var jobIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && !jobSeen.has(en.target)) { jobSeen.add(en.target); queue.push(en.target); }
      });
    }, { threshold: .2 });
    $$('.story, .skills, .record > div').forEach(function (el) { jobIO.observe(el); });
    var contactEl = $('#contact'), footEl = $('footer');
    if (contactEl) new IntersectionObserver(function (e) { contactVisible = e[0].isIntersecting; }, { threshold: .4 }).observe(contactEl);
    if (footEl) new IntersectionObserver(function (e) { footVisible = e[0].isIntersecting; }, { threshold: .1 }).observe(footEl);
  }
  setInterval(function () {
    if (!agentsOn || building || !queue.length || document.hidden) return;
    if (boxes.length < 3) addBox(queue.shift(), { guides: true });
  }, 240);

  /* ---------- Layer tabs: the panel is rebuilt on every switch ---------- */
  $$('.tab-panel').forEach(function (panel) {
    new MutationObserver(function () {
      if (panel.hidden || !agentsOn || building) return;
      flash(panel, 'panel-in', 500);
      var h = $('h4', panel), e = $('.eyebrow', panel), chips = $('.chips', panel);
      if (e) scramble(e, 380);
      if (h) typeFx(h, { dur: 300, delay: 60 });
      if (chips) popChips(chips);
      if (boxes.length < 5) addBox(panel, { draw: 280, hold: 260 });
    }).observe(panel, { attributes: true, attributeFilter: ['hidden'] });
  });

  /* ---------- Project filter: cards glide to their new places ---------- */
  var firstRects = null;
  document.addEventListener('click', function (e) {
    if (!e.target.closest || !e.target.closest('[data-filter]') || !agentsOn) return;
    firstRects = new Map();
    $$('[data-cat]').forEach(function (c) { if (!c.hidden) firstRects.set(c, c.getBoundingClientRect()); });
    requestAnimationFrame(function () {
      $$('[data-cat]').forEach(function (c) {
        if (c.hidden || !c.animate) return;
        var was = firstRects.get(c), now = c.getBoundingClientRect();
        if (c._fx) revealItem(c, true);
        if (was) {
          c.animate([{ transform: 'translate(' + (was.left - now.left) + 'px,' + (was.top - now.top) + 'px)' }, { transform: 'none' }], { duration: 480, easing: 'cubic-bezier(.3,.8,.2,1)' });
        } else {
          c.animate([{ opacity: 0, transform: 'scale(.86)' }, { opacity: 1, transform: 'none' }], { duration: 420, easing: 'cubic-bezier(.3,1.3,.5,1)' });
          if (boxes.length < 5) addBox(c, { draw: 300, hold: 240 });
        }
      });
    });
  }, true);

  /* ---------- Marquee bands, built from words already on the page ---------- */
  function makeBand(reverse) {
    var band = document.createElement('div');
    band.className = 'mq' + (reverse ? ' rev' : '');
    band.setAttribute('aria-hidden', 'true');
    var html = '';
    for (var i = 0; i < 8; i++) html += '<span>BUILT.</span><span>MEASURED.</span><span>SHIPPED.</span>';
    band.innerHTML = '<div class="mq-in"><div class="mq-track">' + html + '</div></div>';
    return band;
  }
  var heroEl = $('.hero');
  if (heroEl) heroEl.parentNode.insertBefore(makeBand(false), heroEl.nextSibling);
  var contactSec = $('#contact');
  if (contactSec) contactSec.parentNode.insertBefore(makeBand(true), contactSec);
  var bands = $$('.mq-in');

  /* ---------- Nav progress and active section ---------- */
  var navEl = $('.nav'), navLinks = $('.nav-links');
  var prog = document.createElement('i');
  prog.className = 'nav-prog';
  prog.setAttribute('aria-hidden', 'true');
  if (navEl) navEl.appendChild(prog);
  var ind = document.createElement('i');
  ind.className = 'nav-ind';
  ind.setAttribute('aria-hidden', 'true');
  if (navLinks) {
    navLinks.appendChild(ind);
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        /* The hero has no nav link, so reaching it clears the indicator. */
        var link = en.target.id ? $('a[href="#' + en.target.id + '"]', navLinks) : null;
        $$('a', navLinks).forEach(function (a) { a.classList.toggle('active', a === link); });
        ind.style.opacity = link ? '1' : '0';
        if (link) {
          ind.style.width = link.offsetWidth + 'px';
          ind.style.transform = 'translateX(' + link.offsetLeft + 'px)';
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    $$('.sec').forEach(function (s) { if (s.id) spy.observe(s); });
    if (heroEl) spy.observe(heroEl);
  }

  /* ---------- Scroll: parallax, band skew, progress, and nothing left hidden ---------- */
  var scrollQueued = false, lastY = window.scrollY, lastFlush = 0, skew = 0;
  function onScrollFrame() {
    scrollQueued = false;
    var y = window.scrollY, max = root.scrollHeight - H;
    if (navEl) navEl.style.setProperty('--p', max > 0 ? (y / max).toFixed(4) : '0');
    if (y < H * 1.4) {
      if (word) {
        word.style.transform = 'translate3d(0,' + (y * .26).toFixed(1) + 'px,0)';
        word.style.setProperty('--fade', clamp(1 - y / (H * 1.1), .15, 1).toFixed(3));
      }
      if (photoWrap) photoWrap.style.transform = 'translate3d(0,' + (y * .06).toFixed(1) + 'px,0)';
    }
    skew = clamp((y - lastY) * .22, -12, 12);
    lastY = y;
    bands.forEach(function (b) { b.style.transform = 'skewX(' + (-skew).toFixed(2) + 'deg)'; });
    clearTimeout(onScrollFrame.t);
    onScrollFrame.t = setTimeout(function () { bands.forEach(function (b) { b.style.transform = ''; }); }, 140);

    /* A jump past a section (anchor link, End key) must not leave anything hidden. */
    var now = performance.now();
    if (now - lastFlush > 180) {
      lastFlush = now;
      armed.slice().forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.height && r.bottom < 0) revealItem(el, true);
      });
    }
  }
  window.addEventListener('scroll', function () {
    if (!scrollQueued) { scrollQueued = true; requestAnimationFrame(onScrollFrame); }
  }, { passive: true });

  /* ---------- Pointer ---------- */
  window.addEventListener('pointermove', function (e) {
    if (e.pointerType === 'mouse') { pointer = { x: e.clientX, y: e.clientY }; pointerMoved = true; }
  }, { passive: true });
  document.addEventListener('mouseleave', function () { pointer = null; });

  /* A click ripples out, and the nearest free agents rush over to look. */
  window.addEventListener('pointerdown', function (e) {
    if (!agentsOn) return;
    ring(e.clientX, e.clientY, RED, 70);
    spark(e.clientX, e.clientY, '#fff', 8);
    agents.filter(function (a) { return !a.job; })
      .sort(function (p, q) { return Math.hypot(p.x - e.clientX, p.y - e.clientY) - Math.hypot(q.x - e.clientX, q.y - e.clientY); })
      .slice(0, 4).forEach(function (a, i) {
        a.tx = e.clientX + Math.cos(i * 1.57) * 34;
        a.ty = e.clientY + Math.sin(i * 1.57) * 34;
        a.nextWander = performance.now() + 1100;
      });
  }, { passive: true });

  if (finePointer) {
    /* Cards: spotlight and travelling border everywhere; tilt on the smaller ones. */
    var hoverCard = null, hoverMag = null;
    var hoverStamp = typeof WeakMap === 'function' ? new WeakMap() : null;
    $$('.btn, .nav-cta, .social, .tab, .link-cta, .ext').forEach(function (el) { el.classList.add('mag'); });
    document.addEventListener('pointermove', function (e) {
      if (e.pointerType !== 'mouse' || !e.target.closest) return;
      var card = e.target.closest('.card');
      if (hoverCard && hoverCard !== card) { hoverCard.style.removeProperty('--rx'); hoverCard.style.removeProperty('--ry'); }
      hoverCard = card;
      if (card) {
        var r = card.getBoundingClientRect(), px = e.clientX - r.left, py = e.clientY - r.top;
        card.style.setProperty('--mx', px + 'px');
        card.style.setProperty('--my', py + 'px');
        if (card.classList.contains('work') && agentsOn) {
          card.style.setProperty('--rx', ((.5 - py / r.height) * 7).toFixed(2) + 'deg');
          card.style.setProperty('--ry', ((px / r.width - .5) * 7).toFixed(2) + 'deg');
        }
      }
      var mag = e.target.closest('.mag');
      if (hoverMag && hoverMag !== mag) hoverMag.style.translate = '';
      hoverMag = mag;
      if (mag && agentsOn) {
        var m = mag.getBoundingClientRect();
        mag.style.translate = ((e.clientX - m.left - m.width / 2) * .22).toFixed(1) + 'px ' + ((e.clientY - m.top - m.height / 2) * .32).toFixed(1) + 'px';
      }
    }, { passive: true });
    document.addEventListener('pointerover', function (e) {
      if (!e.target.closest || !agentsOn || building || e.pointerType !== 'mouse') return;
      /* Monospace labels decode on hover. */
      var label = e.target.closest('.btn:not(#copy), .social, .link-cta, .nav-cta, .ext');
      if (label && !label.children.length && label !== e.relatedTarget && !(e.relatedTarget && label.contains(e.relatedTarget))) scramble(label, 340);
      /* Hovering a card calls the nearest agent over to select it. */
      var card = e.target.closest('.card');
      if (!card || !hoverStamp) return;
      var now = performance.now();
      if (now - (hoverStamp.get(card) || -9999) < 2500 || boxes.length > 3) return;
      hoverStamp.set(card, now);
      addBox(card, { draw: 300, hold: 480 });
    });
  }

  /* ---------- Portrait extras ---------- */
  if (photo) {
    var scan = document.createElement('i');
    scan.className = 'photo-scan';
    scan.setAttribute('aria-hidden', 'true');
    photo.appendChild(scan);
  }

  /* ---------- Copy button feedback ---------- */
  var copyBtn = $('#copy'), copyStatus = $('#copy-status');
  if (copyBtn && copyStatus) {
    var copyLabel = copyBtn.textContent;
    new MutationObserver(function () {
      if (copyStatus.textContent.indexOf('Copied') !== 0) return;
      copyBtn.textContent = 'COPIED ✓';
      if (agentsOn) {
        var r = copyBtn.getBoundingClientRect();
        ring(r.left + r.width / 2, r.top + r.height / 2, '#86efac', 120);
        spark(r.left + r.width / 2, r.top + r.height / 2, '#86efac', 22);
      }
      clearTimeout(copyBtn._t);
      copyBtn._t = setTimeout(function () { copyBtn.textContent = copyLabel; }, 1800);
    }).observe(copyStatus, { childList: true, characterData: true, subtree: true });
  }

  /* ---------- Console ---------- */
  var toggle = $('#toggle-agents');
  toggle.addEventListener('click', function () {
    agentsOn = !agentsOn;
    toggle.setAttribute('aria-pressed', String(agentsOn));
    toggle.textContent = agentsOn ? 'Agents on' : 'Agents off';
    root.classList.toggle('calm', !agentsOn);
    if (agentsOn) { start(); return; }
    finishBuild();
    completeAll();
    flushReveals();
    boxes = [];
    agents.forEach(function (a) { a.job = false; a.mode = 'arrow'; });
    root.classList.remove('rulers');
    rulerA = 0;
    stop();
  });
  $('#rebuild').addEventListener('click', function () {
    if (!agentsOn) toggle.click();
    window.scrollTo({ top: 0, behavior: 'instant' });
    if (word) { word.style.transform = ''; word.style.removeProperty('--fade'); }
    if (photoWrap) photoWrap.style.transform = '';
    flushReveals();
    armAll();
    if (jobSeen) { queue = []; }
    runBuild();
  });

  /* ---------- Go ---------- */
  armAll();
  onScrollFrame();
  if (root.classList.contains('building') && window.scrollY < 80) {
    runBuild();
  } else {
    root.classList.remove('building');
    if (word) word.classList.add('buzz');
    start();
  }
})();
