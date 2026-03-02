// Dark mode toggle
function toggleTheme() {
    document.body.classList.toggle('dark');
    const btn = document.querySelector('.theme-toggle');
    btn.textContent = document.body.classList.contains('dark') ? '☀️' : '🌙';
    localStorage.setItem('theme', document.body.classList.contains('dark') ? 'dark' : 'light');
}

// Load saved theme
if (localStorage.getItem('theme') === 'dark') {
    document.body.classList.add('dark');
    const btn = document.querySelector('.theme-toggle');
    if (btn) btn.textContent = '☀️';
}

// Active nav link
document.addEventListener('DOMContentLoaded', () => {
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.style.background = 'rgba(255,255,255,0.3)';
        }
    });
});
