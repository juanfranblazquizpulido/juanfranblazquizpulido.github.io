// Keep navigation on the photograph, switching to a solid surface over page content.
(() => {
  const header = document.querySelector('.site-header');
  const hero = document.querySelector('.hero');
  if (!header || !hero) return;
  document.documentElement.classList.add('header-enhanced');
  let scheduled = false;
  const update = () => {
    header.classList.toggle('over-content', hero.getBoundingClientRect().bottom <= header.offsetHeight + 1);
    scheduled = false;
  };
  const measure = () => {
    document.documentElement.style.setProperty('--header-height', `${header.offsetHeight}px`);
    update();
  };
  window.addEventListener('scroll', () => {
    if (!scheduled) { scheduled = true; requestAnimationFrame(update); }
  }, { passive: true });
  window.addEventListener('resize', measure);
  window.addEventListener('pageshow', measure);
  if ('ResizeObserver' in window) new ResizeObserver(measure).observe(header);
  measure();
})();
