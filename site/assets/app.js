'use strict';
const themeButton = document.querySelector('.theme-toggle');
function syncThemeLabel() { themeButton?.setAttribute('aria-label', document.documentElement.dataset.theme === 'dark' ? '切换到浅色模式' : '切换到深色模式'); }
syncThemeLabel();
themeButton?.addEventListener('click', () => {
  const theme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
  document.documentElement.dataset.theme = theme;
  try { localStorage.setItem('ai-weekly-theme', theme); } catch (_) {}
  syncThemeLabel();
});
const search = document.querySelector('#search');
const topic = document.querySelector('#topic');
const cards = [...document.querySelectorAll('.archive-card')];
function filterIssues() {
  const words = search.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
  let count = 0;
  cards.forEach(card => {
    const text = card.dataset.search.toLocaleLowerCase();
    const matches = words.every(word => text.includes(word)) && (!topic.value || JSON.parse(card.dataset.tags).includes(topic.value));
    card.hidden = !matches;
    if (matches) count++;
  });
  document.querySelector('#archive-count').textContent = words.length || topic.value ? `找到 ${count} / ${cards.length} 期` : `共 ${cards.length} 期周报`;
  document.querySelector('#empty-state').hidden = count > 0;
}
search?.addEventListener('input', filterIssues);
topic?.addEventListener('change', filterIssues);
document.querySelector('#clear-search')?.addEventListener('click', () => { search.value = ''; topic.value = ''; filterIssues(); search.focus(); });
document.querySelector('.print-button')?.addEventListener('click', () => window.print());
const progress = document.querySelector('#reading-progress');
const headings = [...document.querySelectorAll('.prose h2, .prose h3')];
if (progress) {
  let scheduled = false;
  function updateReading() {
    const extent = document.documentElement.scrollHeight - innerHeight;
    progress.style.width = `${extent > 0 ? Math.min(100, scrollY / extent * 100) : 100}%`;
    const current = headings.filter(h => h.getBoundingClientRect().top <= 150).pop() || headings[0];
    document.querySelectorAll('.toc nav a').forEach(link => {
      const active = link.hash === `#${current?.id}`;
      link.classList.toggle('active', active);
      if (active) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current');
    });
    scheduled = false;
  }
  const schedule = () => { if (!scheduled) { scheduled = true; requestAnimationFrame(updateReading); } };
  addEventListener('scroll', schedule, { passive: true });
  addEventListener('resize', schedule);
  updateReading();
}
