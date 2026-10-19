try { const theme = localStorage.getItem('ai-weekly-theme'); if (theme === 'light' || theme === 'dark') document.documentElement.dataset.theme = theme; } catch (_) {}
