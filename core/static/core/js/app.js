/* hamburger menue */

document.addEventListener('DOMContentLoaded', function () {
  const btn = document.getElementById('navToggle');
  const nav = document.getElementById('siteNav');
  if (!btn || !nav) return;

  function openNav() {
    btn.setAttribute('aria-expanded', 'true');
    nav.classList.add('open');
    nav.setAttribute('aria-hidden', 'false');
  }

  function closeNav() {
    btn.setAttribute('aria-expanded', 'false');
    nav.classList.remove('open');
    nav.setAttribute('aria-hidden', 'true');
  }

  btn.addEventListener('click', function () {
    const expanded = btn.getAttribute('aria-expanded') === 'true';
    if (expanded) closeNav(); else openNav();
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && nav.classList.contains('open')) closeNav();
  });

  document.addEventListener('click', function (e) {
    if (!nav.classList.contains('open')) return;
    if (!nav.contains(e.target) && !btn.contains(e.target)) closeNav();
  });
});
