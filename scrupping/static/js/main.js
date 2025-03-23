// Product Data (Consider moving to Django models/views)
const products = [
    {
        category: 'cars',
        en: { name: 'Luxury Sedan', desc: 'Premium luxury sedan with advanced features' },
        ar: { name: 'سيارة سيدان فاخرة', desc: 'سيارة سيدان فاخرة مع ميزات متقدمة' },
        fr: { name: 'Berline de Luxe', desc: 'Berline de luxe avec caractéristiques avancées' },
        price: 85000,
        image: '/static/images/car1.jpeg' // Updated path for Django static files
    },
    {
        category: 'clothing',
        en: { name: 'Designer Suit', desc: 'Premium tailored business suit' },
        ar: { name: 'بدلة مصمم', desc: 'بدلة عمل مخصّصة عالية الجودة' },
        fr: { name: 'Costume Sur Mesure', desc: 'Costume d\'affaires sur mesure de qualité supérieure' },
        price: 899,
        image: '/static/images/cloth2.jpeg'
    },
    {
        category: 'shoes',
        en: { name: 'Leather Oxfords', desc: 'Handcrafted premium leather shoes' },
        ar: { name: 'أحذية أكسفورد جلدية', desc: 'أحذية جلدية فاخرة مصنوعة يدويًا' },
        fr: { name: 'Derbies en Cuir', desc: 'Chaussures en cuir premium faites main' },
        price: 450,
        image: '/static/images/shos.jpeg'
    },
    {
        category: 'cars',
        en: { name: 'Sports Car', desc: 'High-performance sports vehicle' },
        ar: { name: 'سيارة رياضية', desc: 'مركبة رياضية عالية الأداء' },
        fr: { name: 'Voiture de Sport', desc: 'Véhicule sportif haute performance' },
        price: 12000,
        image: '/static/images/car.jpeg'
    }
];

// Theme Management
function initializeTheme() {
    const themeToggle = document.getElementById('themeToggle');
    const htmlElement = document.documentElement;
    
    const updateThemeIcon = () => {
        const isDark = htmlElement.classList.contains('dark');
        themeToggle.querySelector('i').className = isDark ? 'fas fa-sun me-2' : 'fas fa-moon me-2';
    };

    themeToggle.addEventListener('click', () => {
        htmlElement.classList.toggle('dark');
        localStorage.setItem('theme', htmlElement.classList.contains('dark') ? 'dark' : 'light');
        updateThemeIcon();
        updateThemeText();
    });

    // Load saved theme
    if (localStorage.getItem('theme') === 'dark') {
        htmlElement.classList.add('dark');
    }
    updateThemeIcon();
}

// Language Management
function initializeLanguage() {
    const languageSelect = document.getElementById('languageSelect');
    
    const updateLanguage = () => {
        const lang = languageSelect.value;
        document.querySelectorAll('[data-lang]').forEach(el => {
            el.classList.toggle('hidden', el.dataset.lang !== lang);
        });
        document.documentElement.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr');
        document.documentElement.setAttribute('lang', lang);
        lang === 'ar' ? document.documentElement.classList.add('arabic-font') 
                     : document.documentElement.classList.remove('arabic-font');
        generateProductCards(lang);
        updateThemeText();
    };

    languageSelect.addEventListener('change', () => {
        localStorage.setItem('lang', languageSelect.value);
        updateLanguage();
    });

    // Load saved language
    if (localStorage.getItem('lang')) {
        languageSelect.value = localStorage.getItem('lang');
    }
    updateLanguage();
}

// Product Filtering
function initializeFilters() {
    document.querySelectorAll('.filter-btn').forEach(button => {
        button.addEventListener('click', () => {
            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.classList.remove('bg-amber-600', 'text-white');
                btn.classList.add('bg-gray-200', 'dark:bg-gray-700');
            });
            button.classList.add('bg-amber-600', 'text-white');
            filterProducts(button.dataset.filter);
        });
    });
}

function filterProducts(category) {
    document.querySelectorAll('.product-card').forEach(product => {
        product.style.display = (category === 'all' || product.dataset.category === category) 
            ? 'block' 
            : 'none';
    });
}

// Product Card Generation
function generateProductCards(lang = 'en') {
    const container = document.getElementById('productsContainer');
    container.innerHTML = '';

    products.forEach(product => {
        const card = document.createElement('div');
        card.className = 'product-card bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden hover:shadow-xl';
        card.dataset.category = product.category;

        card.innerHTML = `
            <img src="${product.image}" class="w-full h-56 object-cover" alt="${product[lang].name}">
            <div class="p-6">
                <div class="flex justify-between items-center mb-3">
                    <h3 class="text-xl font-semibold text-gray-800 dark:text-white">
                        ${product[lang].name}
                    </h3>
                    <div class="flex space-x-2">
                        <button class="text-amber-500 hover:text-amber-600">
                            <i class="far fa-heart"></i>
                        </button>
                        <button class="text-blue-500 hover:text-blue-600">
                            <i class="fas fa-share"></i>
                        </button>
                    </div>
                </div>
                <p class="text-gray-600 dark:text-gray-300 mb-4">${product[lang].desc}</p>
                <div class="flex justify-between items-center">
                    <span class="text-2xl font-bold text-amber-500">MRU${product.price.toLocaleString()}</span>
                </div>
            </div>
        `;
        container.appendChild(card);
    });
}

// Theme Text Update
function updateThemeText() {
    const currentLang = document.getElementById('languageSelect').value;
    document.querySelectorAll('#themeToggle [data-lang]').forEach(el => {
        el.classList.toggle('hidden', el.dataset.lang !== currentLang);
    });
}

// Initialization
document.addEventListener('DOMContentLoaded', () => {
    // Set copyright year
    document.getElementById('copyrightYear').textContent = new Date().getFullYear();
    
    // Initialize components
    initializeTheme();
    initializeLanguage();
    initializeFilters();
    
    // Generate initial product cards
    generateProductCards();
    document.querySelector('.filter-btn[data-filter="all"]').click();
});