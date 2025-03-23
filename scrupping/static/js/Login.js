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

// Password Visibility Toggle
const passwordInput = document.getElementById('passwordInput');
const togglePassword = document.getElementById('togglePassword');

togglePassword.addEventListener('click', () => {
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);
    togglePassword.querySelector('i').classList.toggle('fa-eye-slash');
});

// Initialize
document.getElementById('copyrightYear').textContent = new Date().getFullYear();

// Load preferences
if (localStorage.getItem('theme') === 'dark') {
    htmlElement.classList.add('dark');
}

if (localStorage.getItem('lang')) {
    languageSelect.value = localStorage.getItem('lang');
}

updateThemeIcon();
updateLanguage();

// Form submission handling
document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const formData = new FormData(this);
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    // Convert FormData to a plain object
    const formDataObj = {};
    formData.forEach((value, key) => {
        formDataObj[key] = value;
    });
    
    fetch('/login/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(formDataObj)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Login successful
            
            // Store tokens in localStorage
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);
            
            // Redirect to landing page
            window.location.href = data.redirect_url;
        } else {
            // Show error message
            const errorDiv = document.getElementById('errorMessage');
            errorDiv.textContent = data.error || "Login failed";
            errorDiv.classList.remove('hidden');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('errorMessage').textContent = "An error occurred during login";
        document.getElementById('errorMessage').classList.remove('hidden');
    });
});