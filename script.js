/* =========================================
   REPAIR CAFÉ OF THE PENINSULA — Script
   ========================================= */

// --- Header border once the page scrolls ---
const header = document.querySelector('.site-header');
function updateHeader() {
  header.classList.toggle('is-scrolled', window.scrollY > 8);
}
window.addEventListener('scroll', updateHeader, { passive: true });
updateHeader(); // run immediately so hash-linked page loads show the border

// --- Mobile menu ---
const menuToggle = document.querySelector('.menu-toggle');
const siteNav = document.getElementById('site-nav');

function setMenu(open) {
  menuToggle.setAttribute('aria-expanded', String(open));
  siteNav.classList.toggle('is-open', open);
  document.body.classList.toggle('menu-open', open);
}

menuToggle.addEventListener('click', () => {
  setMenu(menuToggle.getAttribute('aria-expanded') !== 'true');
});
siteNav.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => setMenu(false));
});
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && siteNav.classList.contains('is-open')) {
    setMenu(false);
    menuToggle.focus();
  }
});
// close the menu if the window grows past the mobile breakpoint
window.matchMedia('(min-width: 881px)').addEventListener('change', (e) => {
  if (e.matches) setMenu(false);
});
