// Theme Toggle
const themeToggle = document.getElementById('themeToggle');
const htmlElement = document.documentElement;

function updateThemeIcon() {
    const isDark = htmlElement.classList.contains('dark');
    themeToggle.querySelector('i').className = isDark ? 'fas fa-sun me-2' : 'fas fa-moon me-2';
}

themeToggle.addEventListener('click', () => {
    htmlElement.classList.toggle('dark');
    updateThemeIcon();
    updateThemeText();
    localStorage.setItem('theme', htmlElement.classList.contains('dark') ? 'dark' : 'light');
});

// Language Switch
const languageSelect = document.getElementById('languageSelect');

function updateLanguage() {
    const lang = languageSelect.value;
    document.querySelectorAll('[data-lang]').forEach(el => {
        el.classList.toggle('hidden', el.dataset.lang !== lang);
    });
    htmlElement.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr');
    htmlElement.setAttribute('lang', lang);
    lang === 'ar' ? htmlElement.classList.add('arabic-font') : htmlElement.classList.remove('arabic-font');
    localStorage.setItem('lang', lang);
}

languageSelect.addEventListener('change', updateLanguage);

// Initialize
document.getElementById('copyrightYear').textContent = new Date().getFullYear();

// Load saved preferences
if (localStorage.getItem('theme') === 'dark') {
    htmlElement.classList.add('dark');
}
if (localStorage.getItem('lang')) {
    languageSelect.value = localStorage.getItem('lang');
}

updateThemeIcon();
updateLanguage();