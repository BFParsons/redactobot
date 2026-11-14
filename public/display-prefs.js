// Apply the saved display choices (theme, colours, motion) before the page draws, so it does not
// flash the wrong theme. Same-origin file because the page's CSP blocks inline scripts.
try {
  const p = JSON.parse(localStorage.getItem('redactobot.display.v1') || '{}');
  const root = document.documentElement;
  if (p.theme === 'light' || p.theme === 'dark') root.dataset.theme = p.theme;
  if (p.palette === 'cb') root.dataset.palette = 'cb';
  if (p.motion === 'reduced') root.dataset.motion = 'reduced';
} catch { /* storage unavailable: system settings apply */ }
