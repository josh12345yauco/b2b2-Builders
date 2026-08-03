/* Paiz Builders — homepage behavior
   Nav scroll state, mobile menu, scroll reveals, Project Builder. */

(function () {
  'use strict';

  // Flag JS availability so reveal styles only apply when they can be undone.
  document.documentElement.classList.add('js');

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Hero background video: respect reduced motion ---------- */
  var heroVideo = document.querySelector('.hero-v2 video');
  if (heroVideo && reduceMotion) {
    heroVideo.removeAttribute('autoplay');
    heroVideo.pause();
  }

  /* ---------- dataLayer helper (guard for undefined dataLayer) ---------- */
  function trackEvent(payload) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(payload);
  }

  /* ---------- Sticky nav: hairline border on scroll ---------- */
  var header = document.getElementById('site-header');

  function onScroll() {
    header.classList.toggle('is-scrolled', window.scrollY > 8);
    healMissedReveals();
  }
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ---------- Mobile menu ---------- */
  var navToggle = document.getElementById('nav-toggle');
  var mobileMenu = document.getElementById('mobile-menu');

  function setMenu(open) {
    navToggle.setAttribute('aria-expanded', String(open));
    navToggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    mobileMenu.hidden = !open;
    document.body.style.overflow = open ? 'hidden' : '';
  }

  navToggle.addEventListener('click', function () {
    setMenu(navToggle.getAttribute('aria-expanded') !== 'true');
  });

  mobileMenu.addEventListener('click', function (e) {
    if (e.target.closest('a')) setMenu(false);
  });

  var menuClose = document.getElementById('mobile-menu-close');
  if (menuClose) {
    menuClose.addEventListener('click', function () {
      setMenu(false);
      navToggle.focus();
    });
  }

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && navToggle.getAttribute('aria-expanded') === 'true') {
      setMenu(false);
      navToggle.focus();
    }
  });

  /* ---------- Scroll reveals ---------- */
  var revealEls = Array.prototype.slice.call(document.querySelectorAll('[data-reveal]'));

  if (reduceMotion || !('IntersectionObserver' in window)) {
    revealEls.forEach(function (el) { el.classList.add('revealed'); });
    revealEls = [];
  } else {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        // Reveal on intersection, and also if the element was jumped past
        // (fast scrolls and anchor jumps can skip the intersection frame).
        if (entry.isIntersecting || entry.boundingClientRect.bottom < 0) {
          entry.target.classList.add('revealed');
          observer.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.1 });

    revealEls.forEach(function (el) { observer.observe(el); });
  }

  // Self-heal on scroll: anything at or above the reveal line becomes visible,
  // even if the observer never saw it cross the viewport.
  function healMissedReveals() {
    if (!revealEls.length) return;
    var line = window.innerHeight * 0.95;
    revealEls = revealEls.filter(function (el) {
      if (el.classList.contains('revealed')) return false;
      if (el.getBoundingClientRect().top < line) {
        el.classList.add('revealed');
        return false;
      }
      return true;
    });
  }

  // Initial state: header border + reveals for pages that load mid-scroll
  onScroll();

  /* ---------- Project Builder ---------- */
  var form = document.getElementById('pb-form');
  if (!form) return;

  var steps = Array.prototype.slice.call(form.querySelectorAll('.builder-step'));
  var progressBar = document.getElementById('builder-progressbar');
  var progressFill = document.getElementById('builder-progress-fill');
  var stepLabel = document.getElementById('builder-step-label');
  var backBtn = document.getElementById('builder-back');
  var nextBtn = document.getElementById('builder-next');
  var submitBtn = document.getElementById('builder-submit');
  var controls = document.getElementById('builder-controls');
  var successPanel = document.getElementById('builder-success');
  var TOTAL = steps.length;
  var current = 1; // 1-based

  function stepEl(n) {
    return steps[n - 1];
  }

  function setError(fieldset, show) {
    var error = fieldset.querySelector('.builder-error');
    if (error) error.hidden = !show;
  }

  function checked(name) {
    return form.querySelector('input[name="' + name + '"]:checked');
  }

  function validateStep(n) {
    var fs = stepEl(n);
    var ok = true;

    if (n === 1) {
      ok = !!checked('projectType');
    } else if (n === 2) {
      ok = !!checked('projectSize');
    } else if (n === 3) {
      ok = !!checked('propertyType') && !!checked('ownership');
    } else if (n === 4) {
      ok = !!checked('timeline') && !!checked('budget');
    } else if (n === 5) {
      ok = document.getElementById('pb-location').value.trim().length > 0;
    } else if (n === 6) {
      var emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(document.getElementById('pb-email').value.trim());
      ok = document.getElementById('pb-name').value.trim().length > 0 &&
           document.getElementById('pb-phone').value.trim().length >= 7 &&
           emailOk &&
           !!checked('contactPref');
    }

    setError(fs, !ok);
    return ok;
  }

  /* Size examples adapt to the chosen project type */
  var SIZE_HINTS = {
    'Kitchen': {
      small: 'Refresh or galley — under 100 sq ft',
      medium: 'Typical rowhome kitchen — 100\u2013200 sq ft',
      large: 'Open-plan or addition — 200+ sq ft'
    },
    'Bathroom': {
      small: 'Powder room — under 40 sq ft',
      medium: 'Full bath — 40\u201375 sq ft',
      large: 'Primary suite — 75+ sq ft'
    },
    'Full Build / Remodel': {
      small: 'One floor or unit — under 800 sq ft',
      medium: 'Whole rowhome — 800\u20131,800 sq ft',
      large: 'Gut + addition or ground-up — 1,800+ sq ft'
    },
    'Concrete': {
      small: 'Sidewalk or steps — under 200 sq ft',
      medium: 'Patio or garage pad — 200\u2013600 sq ft',
      large: 'Foundation or full flatwork — 600+ sq ft'
    },
    'Framing': {
      small: 'Repair — a few joists or one header',
      medium: 'Wall removal or partial reframe',
      large: 'Full framing package or addition'
    },
    'Something else': {
      small: 'A day or two of work',
      medium: 'About a week of work',
      large: 'A multi-week project'
    }
  };

  function refreshSizeHints() {
    var type = checked('projectType');
    var hints = SIZE_HINTS[type ? type.value : ''] || { small: 'A compact scope', medium: 'The typical project', large: 'The big one' };
    form.querySelectorAll('[data-size-hint]').forEach(function (el) {
      el.textContent = hints[el.getAttribute('data-size-hint')];
    });
  }

  form.addEventListener('change', function (e) {
    if (e.target.name === 'projectType') refreshSizeHints();
  });
  refreshSizeHints();

  /* Dictation for the notes field (Web Speech API, hidden if unsupported) */
  var dictateBtn = document.getElementById('pb-dictate');
  var notesEl = document.getElementById('pb-notes');
  var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (dictateBtn && notesEl && SR) {
    dictateBtn.hidden = false;
    var rec = null;
    var listening = false;

    function stopDictation() {
      listening = false;
      if (rec) { try { rec.stop(); } catch (err) {} }
      dictateBtn.classList.remove('listening');
      dictateBtn.setAttribute('aria-pressed', 'false');
      dictateBtn.querySelector('.dictate-label').textContent = 'Dictate';
    }

    dictateBtn.addEventListener('click', function () {
      if (listening) { stopDictation(); return; }
      rec = new SR();
      rec.lang = 'en-US';
      rec.continuous = true;
      rec.interimResults = false;
      rec.onresult = function (ev) {
        for (var i = ev.resultIndex; i < ev.results.length; i++) {
          if (ev.results[i].isFinal) {
            var txt = ev.results[i][0].transcript.trim();
            if (txt) notesEl.value = (notesEl.value ? notesEl.value.replace(/\s+$/, '') + ' ' : '') + txt;
          }
        }
      };
      rec.onend = stopDictation;
      rec.onerror = stopDictation;
      listening = true;
      dictateBtn.classList.add('listening');
      dictateBtn.setAttribute('aria-pressed', 'true');
      dictateBtn.querySelector('.dictate-label').textContent = 'Listening\u2026 tap to stop';
      rec.start();
    });
  }

  function showStep(n, focusHeading) {
    steps.forEach(function (fs) {
      var isTarget = Number(fs.dataset.step) === n;
      fs.hidden = !isTarget;
      fs.classList.toggle('step-in', isTarget && !reduceMotion);
    });

    current = n;
    progressFill.style.width = (n / TOTAL) * 100 + '%';
    progressBar.setAttribute('aria-valuenow', String(n));
    stepLabel.textContent = 'Step ' + n + ' of ' + TOTAL;

    backBtn.hidden = n === 1;
    nextBtn.hidden = n === TOTAL;
    submitBtn.hidden = n !== TOTAL;

    if (focusHeading) {
      var legend = stepEl(n).querySelector('.builder-q');
      if (legend) legend.focus();
    }
  }

  nextBtn.addEventListener('click', function () {
    if (!validateStep(current)) return;
    trackEvent({
      event: 'project_builder_step',
      step: current,
      stepName: stepEl(current).querySelector('.builder-q').textContent
    });
    showStep(current + 1, true);
  });

  backBtn.addEventListener('click', function () {
    setError(stepEl(current), false);
    showStep(current - 1, true);
  });

  // Clear a step's error as soon as the user makes a choice
  form.addEventListener('change', function (e) {
    var fs = e.target.closest('.builder-step');
    if (fs) setError(fs, false);
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!validateStep(TOTAL)) return;

    var payload = {
      projectType: checked('projectType').value,
      projectSize: checked('projectSize').value,
      propertyType: checked('propertyType').value,
      ownership: checked('ownership').value,
      timeline: checked('timeline').value,
      budget: checked('budget').value,
      location: document.getElementById('pb-location').value.trim(),
      notes: document.getElementById('pb-notes').value.trim(),
      name: document.getElementById('pb-name').value.trim(),
      phone: document.getElementById('pb-phone').value.trim(),
      email: document.getElementById('pb-email').value.trim(),
      contactPref: checked('contactPref').value,
      source: 'project-builder'
    };

    // Persist the lead to the site backend (shows in /admin)
    fetch('/api/lead', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      keepalive: true
    }).catch(function () { /* backend offline — payload still tracked below */ });

    trackEvent({ event: 'project_builder_submit', payload: payload });

    steps.forEach(function (fs) { fs.hidden = true; });
    controls.hidden = true;
    stepLabel.textContent = 'Done';
    progressFill.style.width = '100%';
    progressBar.setAttribute('aria-valuenow', String(TOTAL));
    successPanel.hidden = false;
    successPanel.focus();
  });

  showStep(1, false);
})();

/* ==========================================================================
   Internal pages — active nav, project filters, contact form.
   Same patterns as the homepage: dataLayer events + GHL webhook stubs.
   ========================================================================== */

(function () {
  'use strict';

  function trackEvent(payload) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(payload);
  }

  /* ---------- Reliable fragment landing on page load ----------
     With CSS smooth-scrolling, cross-page anchor navigation (e.g.
     /contact/ → /#project-builder) can fail to land. Jump instantly. */
  if (window.location.hash) {
    var target = document.getElementById(window.location.hash.slice(1));
    if (target) {
      // Stop the browser's scroll restoration from racing the jump
      if ('scrollRestoration' in window.history) {
        window.history.scrollRestoration = 'manual';
      }
      var jumpToTarget = function () {
        var top = target.getBoundingClientRect().top + window.pageYOffset - 96;
        window.scrollTo({ top: top, behavior: 'instant' });
      };
      window.requestAnimationFrame(jumpToTarget);
      window.addEventListener('load', function () {
        window.setTimeout(jumpToTarget, 60);
      });
    }
  }

  /* ---------- Active nav state from current path ---------- */
  var section = window.location.pathname.split('/').filter(Boolean)[0] || '';
  if (section) {
    var activeLink = document.querySelector('.nav-links a[data-nav="' + section + '"]');
    if (activeLink) activeLink.classList.add('active');
  }

  /* ---------- Projects hub filter chips (links stay crawlable) ---------- */
  var chipBar = document.getElementById('project-filters');
  if (chipBar) {
    var chips = chipBar.querySelectorAll('.filter-chip');
    var cards = document.querySelectorAll('[data-project-type]');

    chipBar.addEventListener('click', function (e) {
      var chip = e.target.closest('.filter-chip');
      if (!chip) return;
      var filter = chip.dataset.filter;

      chips.forEach(function (c) {
        c.setAttribute('aria-pressed', String(c === chip));
      });
      cards.forEach(function (card) {
        var types = card.dataset.projectType.split(' ');
        card.hidden = filter !== 'all' && types.indexOf(filter) === -1;
      });
      trackEvent({ event: 'project_filter', filter: filter });
    });
  }

  /* ---------- Area landing page lead form ---------- */
  var leadForm = document.getElementById('area-lead-form');
  if (leadForm) {
    leadForm.addEventListener('submit', function (e) {
      e.preventDefault();

      var payload = {
        name: leadForm.querySelector('#lf-name').value.trim(),
        phone: leadForm.querySelector('#lf-phone').value.trim(),
        projectType: leadForm.querySelector('#lf-type').value,
        zip: leadForm.querySelector('#lf-zip').value.trim(),
        budget: leadForm.querySelector('#lf-budget').value,
        timeline: leadForm.querySelector('#lf-timeline').value,
        notes: leadForm.querySelector('#lf-notes').value.trim(),
        area: leadForm.dataset.area || '',
        source: 'area-landing-form'
      };

      var errorEl = leadForm.querySelector('.builder-error');
      if (!payload.name || payload.phone.length < 7 || payload.zip.length < 5) {
        if (errorEl) errorEl.hidden = false;
        return;
      }
      if (errorEl) errorEl.hidden = true;

      // Persist the lead to the site backend (shows in /admin)
      fetch('/api/lead', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        keepalive: true
      }).catch(function () { /* backend offline — payload still tracked below */ });

      trackEvent({ event: 'area_lead_submit', payload: payload });

      leadForm.querySelectorAll('.field, .field-row, .builder-controls').forEach(function (el) {
        el.hidden = true;
      });
      var success = leadForm.querySelector('.form-success');
      if (success) {
        success.hidden = false;
        success.setAttribute('tabindex', '-1');
        success.focus();
      }
    });
  }

  /* ---------- Contact page form ---------- */
  var contactForm = document.getElementById('contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', function (e) {
      e.preventDefault();

      var payload = {
        name: contactForm.querySelector('#cf-name').value.trim(),
        phone: contactForm.querySelector('#cf-phone').value.trim(),
        email: contactForm.querySelector('#cf-email').value.trim(),
        projectType: contactForm.querySelector('#cf-type').value,
        message: contactForm.querySelector('#cf-message').value.trim(),
        source: 'contact-page-form'
      };

      var emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(payload.email);
      var errorEl = contactForm.querySelector('.builder-error');
      if (!payload.name || payload.phone.length < 7 || !emailOk) {
        if (errorEl) errorEl.hidden = false;
        return;
      }
      if (errorEl) errorEl.hidden = true;

      // Persist the lead to the site backend (shows in /admin)
      fetch('/api/lead', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        keepalive: true
      }).catch(function () { /* backend offline — payload still tracked below */ });

      trackEvent({ event: 'contact_form_submit', payload: payload });

      contactForm.querySelectorAll('.field, .field-row, .builder-controls, button[type="submit"]').forEach(function (el) {
        el.hidden = true;
      });
      var success = contactForm.querySelector('.form-success');
      if (success) {
        success.hidden = false;
        success.setAttribute('tabindex', '-1');
        success.focus();
      }
    });
  }
})();

/* ---------- Mobile: sticky horizontal scroll for the services row ----------
   The section pins under the header; vertical scroll drives the cards
   horizontally, then the page resumes normal scrolling. Falls back to the
   plain swipe row on desktop, reduced-motion, or no-JS. */
(function () {
  var section = document.querySelector('.section.services');
  if (!section) return;
  var container = section.querySelector('.container');
  var row = section.querySelector('.services-row');
  if (!container || !row) return;

  var mq = window.matchMedia('(max-width: 960px)');
  var rm = window.matchMedia('(prefers-reduced-motion: reduce)');
  var active = false;
  var start = 0;
  var dist = 1;

  function measure() {
    if (!active) return;
    row.style.transform = '';
    section.style.height = '';
    var header = document.getElementById('site-header');
    var topOffset = header ? header.offsetHeight : 0;
    dist = row.scrollWidth - row.clientWidth;
    if (dist <= 0) { deactivate(); return; }
    container.style.top = topOffset + 'px';
    section.style.height = (container.offsetHeight + dist + topOffset) + 'px';
    start = section.getBoundingClientRect().top + window.scrollY - topOffset;
    onScroll();
  }

  function onScroll() {
    if (!active) return;
    var p = (window.scrollY - start) / dist;
    p = Math.max(0, Math.min(1, p));
    row.style.transform = 'translate3d(' + (-p * dist).toFixed(1) + 'px, 0, 0)';
  }

  function activate() {
    if (active) return;
    active = true;
    section.classList.add('svc-sticky');
    measure();
  }

  function deactivate() {
    active = false;
    section.classList.remove('svc-sticky');
    section.style.height = '';
    container.style.top = '';
    row.style.transform = '';
  }

  function update() {
    if (mq.matches && !rm.matches) { activate(); } else { deactivate(); }
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', function () { if (active) measure(); });
  window.addEventListener('load', function () { if (active) measure(); });
  if (mq.addEventListener) { mq.addEventListener('change', update); } else { mq.addListener(update); }
  update();
})();

/* ---------- Call-click tracking ----------
   Logs every tap on a tel: link (call bar, header button, footer, CTAs)
   to the leads backend so /admin can show call activity. */
(function () {
  'use strict';
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href^="tel:"]');
    if (!a) return;
    try {
      var payload = JSON.stringify({
        page: window.location.pathname,
        label: (a.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 60) || 'call link'
      });
      if (navigator.sendBeacon) {
        navigator.sendBeacon('/api/call', new Blob([payload], { type: 'application/json' }));
      } else {
        fetch('/api/call', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: payload,
          keepalive: true
        }).catch(function () {});
      }
    } catch (err) { /* tracking must never block the call */ }
  });
})();
