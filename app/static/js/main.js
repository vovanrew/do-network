// Головний JavaScript файл

// Функція для додавання плавної прокрутки
function smoothScroll(target) {
    const element = document.querySelector(target);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Ініціалізація при завантаженні сторінки
document.addEventListener('DOMContentLoaded', function() {
    // Плавна прокрутка для якорів
    const anchors = document.querySelectorAll('a[href^="#"]');
    anchors.forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = this.getAttribute('href');
            smoothScroll(target);
        });
    });

    // Показ/приховування навігації при прокрутці на мобільних
    let lastScrollTop = 0;
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', function() {
        if (window.innerWidth <= 768) {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            if (scrollTop > lastScrollTop && scrollTop > 100) {
                // Прокрутка вниз
                navbar.style.transform = 'translateY(-100%)';
            } else {
                // Прокрутка вгору
                navbar.style.transform = 'translateY(0)';
            }
            
            lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
        }
    });

    // Анімація для карток при появі
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Спостереження за картками
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(card);
    });

    // Підсвічування активної сторінки в навігації
    const currentLocation = location.pathname;
    const menuItems = document.querySelectorAll('.nav-link');
    
    menuItems.forEach(item => {
        if (item.getAttribute('href') === currentLocation) {
            item.classList.add('active');
        }
    });

    // Підтвердження при виході зі сторінки створення
    const createForm = document.querySelector('form[action*="create"]');
    if (createForm) {
        let formChanged = false;
        
        createForm.addEventListener('change', function() {
            formChanged = true;
        });
        
        window.addEventListener('beforeunload', function(e) {
            if (formChanged) {
                e.preventDefault();
                e.returnValue = '';
            }
        });
        
        createForm.addEventListener('submit', function() {
            formChanged = false;
        });
    }

    // Додавання класу для touch пристроїв
    if ('ontouchstart' in window) {
        document.body.classList.add('touch-device');
    }

    // Закриття мобільного меню при кліку поза ним
    document.addEventListener('click', function(event) {
        const navbar = document.querySelector('.navbar-collapse');
        const toggler = document.querySelector('.navbar-toggler');
        
        if (navbar && navbar.classList.contains('show')) {
            if (!navbar.contains(event.target) && !toggler.contains(event.target)) {
                toggler.click();
            }
        }
    });
});

// Функція для форматування дати
function formatDate(date) {
    const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return date.toLocaleDateString('uk-UA', options);
}

// Експорт функцій для використання в інших скриптах
window.appUtils = {
    smoothScroll,
    formatDate
};
