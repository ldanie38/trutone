/* hamburger menue */

document.addEventListener('DOMContentLoaded', function () {
  const btn = document.getElementById('navToggle');
  const nav = document.getElementById('siteNav');

  if (!btn || !nav) return;

  btn.addEventListener('click', function () {
    const isOpen = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', String(isOpen));
    nav.setAttribute('aria-hidden', String(!isOpen));
  });
});
