function showToast(message, type = 'success') {
    const existing = document.querySelector('.toast');
    if (existing) existing.remove();
    const toast = document.createElement('div');
    toast.className = 'toast';
    const bg = type === 'success' ? '#2d6a4f' : type === 'error' ? '#e63946' : '#40916c';
    toast.style.cssText = `position:fixed;bottom:88px;right:28px;padding:12px 20px;border-radius:10px;color:white;font-size:0.9em;font-weight:500;z-index:9999;box-shadow:0 4px 16px rgba(0,0,0,0.2);animation:slideIn 0.3s ease;max-width:280px;background:${bg};`;
    const icons = { success: '✅', error: '❌', info: 'ℹ️' };
    toast.textContent = (icons[type] || '') + ' ' + message;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function toggleTheme() {
    document.body.classList.toggle('dark');
    const btn = document.querySelector('.theme-toggle');
    btn.textContent = document.body.classList.contains('dark') ? '☀️' : '🌙';
    localStorage.setItem('theme', document.body.classList.contains('dark') ? 'dark' : 'light');
}

if (localStorage.getItem('theme') === 'dark') {
    document.body.classList.add('dark');
    const btn = document.querySelector('.theme-toggle');
    if (btn) btn.textContent = '☀️';
}

document.addEventListener('DOMContentLoaded', () => {
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath) link.classList.add('active');
    });

    document.querySelectorAll('a[href]').forEach(a => {
        const href = a.getAttribute('href');
        if (href && !href.startsWith('#') && !href.startsWith('javascript') && !href.startsWith('mailto') && !href.startsWith('http')) {
            a.addEventListener('click', e => {
                e.preventDefault();
                const mc = document.querySelector('.main-content');
                if (mc) mc.style.animation = 'fadeOut 0.2s ease forwards';
                setTimeout(() => { window.location.href = href; }, 180);
            });
        }
    });
});
