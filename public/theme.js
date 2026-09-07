// Apply the saved preference before styles render; default to the system setting.
(() => {
  const key = 'academic-site-theme';
  const modes = ['system', 'light', 'dark'];
  const labels = { system: 'Auto', light: 'Light', dark: 'Dark' };
  const icons = { system: '◐', light: '☀', dark: '☾' };
  const system = window.matchMedia('(prefers-color-scheme: dark)');
  let mode = 'system';
  try { const saved = localStorage.getItem(key); if (modes.includes(saved)) mode = saved; } catch {}
  const apply = () => {
    const resolved = mode === 'system' ? (system.matches ? 'dark' : 'light') : mode;
    document.documentElement.dataset.theme = resolved;
    document.documentElement.style.colorScheme = resolved;
    document.querySelectorAll('meta[name="theme-color"]').forEach(meta => {
      meta.content = resolved === 'dark' ? '#101b29' : '#ffffff';
    });
    const button = document.getElementById('theme-toggle');
    if (button) {
      const next = modes[(modes.indexOf(mode) + 1) % modes.length];
      button.hidden = false;
      button.textContent = icons[mode];
      button.setAttribute('aria-label', `Colour theme: ${labels[mode]}. Switch to ${labels[next]}`);
      button.title = `Theme: ${labels[mode]} · Click for ${labels[next]}`;
    }
  };
  apply();
  system.addEventListener('change', apply);
  window.addEventListener('storage', event => {
    if (event.key === key || event.key === null) { mode = modes.includes(event.newValue) ? event.newValue : 'system'; apply(); }
  });
  document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('theme-toggle')?.addEventListener('click', () => {
      mode = modes[(modes.indexOf(mode) + 1) % modes.length];
      try { localStorage.setItem(key, mode); } catch {}
      apply();
    });
    apply();
  });
})();
