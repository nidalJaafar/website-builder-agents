// Enhanced Smooth Scrolling with Offset (Cross-browser compatible)
function smoothScrollTo(targetElement, offset) {
    offset = offset || 0;
    const elementPosition = targetElement.getBoundingClientRect().top + window.pageYOffset;
    const offsetPosition = elementPosition - offset;
    
    // Feature detection for smooth scrolling
    if ('scrollBehavior' in document.documentElement.style) {
        window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
        });
    } else {
        // Fallback for browsers that don't support smooth scrolling
        window.scrollTo(0, offsetPosition);
    }
}

// Enhanced Mobile Menu with Animation
class MobileMenu {
    constructor() {
        this.menuToggle = document.querySelector('.mobile-menu-toggle');
        this.navMenu = document.querySelector('.nav-menu');
        this.init();
    }
    
    init() {
        this.menuToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            this.toggleMenu();
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', (e) => this.handleClickOutside(e));
        
        // Close menu when clicking on nav links
        this.navMenu.addEventListener('click', (e) => {
            if (e.target.tagName === 'A') {
                this.closeMenuWithAnimation();
            }
        });
        
        // Handle window resize
        window.addEventListener('resize', () => this.handleResize());
    }
    
    toggleMenu() {
        this.menuToggle.classList.toggle('active');
        this.navMenu.classList.toggle('active');
        
        // Toggle body scroll and add animation class
        if (this.navMenu.classList.contains('active')) {
            document.body.style.overflow = 'hidden';
            this.navMenu.style.animation = 'slideInRight 0.3s ease-out';
        } else {
            document.body.style.overflow = '';
            this.navMenu.style.animation = 'slideOutRight 0.3s ease-out';
        }
    }
    
    closeMenuWithAnimation() {
        this.menuToggle.classList.remove('active');
        this.navMenu.style.animation = 'slideOutRight 0.3s ease-out';
        
        setTimeout(() => {
            this.navMenu.classList.remove('active');
            this.navMenu.style.animation = '';
            document.body.style.overflow = '';
        }, 280);
    }
    
    handleClickOutside(e) {
        if (this.navMenu.classList.contains('active') && 
            !this.menuToggle.contains(e.target) && 
            !this.navMenu.contains(e.target)) {
            this.closeMenuWithAnimation();
        }
    }
    
    handleResize() {
        // Close menu on desktop if window is resized larger
        if (window.innerWidth > 768 && this.navMenu.classList.contains('active')) {
            this.closeMenuWithAnimation();
        }
    }
}

// Scroll Animation Observer
class ScrollAnimator {
    constructor() {
        this.observer = null;
        this.init();
    }
    
    init() {
        const options = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        this.observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, options);
        
        // Observe elements with animation classes
        document.querySelectorAll('.menu-item, .contact-item, .hours-item').forEach(el => {
            this.observer.observe(el);
        });
    }
}

// Enhanced Navigation with Scroll Spy
class NavigationManager {
    constructor() {
        this.sections = document.querySelectorAll('section[id]');
        this.navLinks = document.querySelectorAll('.nav-menu a[href^="#"]');
        this.headerHeight = document.querySelector('.main-header').offsetHeight;
        this.init();
    }
    
    init() {
        // Smooth scroll for navigation links
        this.navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = link.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    smoothScrollTo(targetElement, this.headerHeight);
                }
            });
        });
        
        // Highlight active section
        window.addEventListener('scroll', () => this.highlightActiveSection());
        this.highlightActiveSection(); // Initial call
    }
    
    highlightActiveSection() {
        const scrollPosition = window.scrollY + this.headerHeight + 50;
        
        this.sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                this.navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }
}

// Interactive Elements Enhancement
class InteractiveEnhancer {
    constructor() {
        this.init();
    }
    
    init() {
        this.addHoverEffects();
        this.addClickAnimations();
        this.setupFormInteractions();
    }
    
    addHoverEffects() {
        // Add hover effects to interactive elements
        const interactiveElements = document.querySelectorAll(
            '.cta-button, .menu-item, .contact-item, .social-link'
        );
        
        interactiveElements.forEach(el => {
            el.addEventListener('mouseenter', () => {
                el.style.transform = 'translateY(-2px)';
                el.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
            });
            
            el.addEventListener('mouseleave', () => {
                el.style.transform = '';
                el.style.boxShadow = '';
            });
        });
    }
    
    addClickAnimations() {
        // Add click animations to buttons
        const buttons = document.querySelectorAll('button, .cta-button');
        
        buttons.forEach(button => {
            button.addEventListener('click', () => {
                button.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    button.style.transform = '';
                }, 150);
            });
        });
    }
    
    setupFormInteractions() {
        // Newsletter form enhancement
        const newsletterInput = document.querySelector('.newsletter-input');
        const newsletterBtn = document.querySelector('.newsletter-btn');
        
        if (newsletterInput && newsletterBtn) {
            newsletterInput.addEventListener('focus', () => {
                newsletterInput.parentElement.classList.add('focused');
            });
            
            newsletterInput.addEventListener('blur', () => {
                if (!newsletterInput.value) {
                    newsletterInput.parentElement.classList.remove('focused');
                }
            });
            
            newsletterBtn.addEventListener('click', () => {
                if (newsletterInput.value && newsletterInput.checkValidity()) {
                    this.showSuccessMessage(newsletterInput.parentElement, 'Subscribed successfully!');
                    newsletterInput.value = '';
                }
            });
        }
    }
    
    showSuccessMessage(container, message) {
        const successMsg = document.createElement('div');
        successMsg.className = 'success-message';
        successMsg.textContent = message;
        successMsg.style.cssText = `
            background: #4CAF50;
            color: white;
            padding: 8px 12px;
            border-radius: 4px;
            margin-top: 8px;
            font-size: 14px;
            animation: fadeInUp 0.3s ease-out;
        `;
        
        container.appendChild(successMsg);
        
        setTimeout(() => {
            successMsg.style.animation = 'fadeOutDown 0.3s ease-out';
            setTimeout(() => successMsg.remove(), 300);
        }, 3000);
    }
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    try {
        // Initialize all components with error handling
        if (document.querySelector('.mobile-menu-toggle')) {
            new MobileMenu();
        }
        
        if (document.querySelector('.nav-menu')) {
            new NavigationManager();
        }
        
        if (document.querySelector('.menu-item, .contact-item, .hours-item')) {
            new ScrollAnimator();
        }
        
        new InteractiveEnhancer();
        
        // Add CSS animations
        addCustomAnimations();
        
        // Performance optimization
        optimizePerformance();
        
    } catch (error) {
        console.error('Error initializing components:', error);
        // Graceful degradation - ensure basic functionality still works
        setupFallbackNavigation();
    }
});

// Fallback navigation for when JavaScript fails
function setupFallbackNavigation() {
    const navLinks = document.querySelectorAll('.nav-menu a[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView();
            }
        });
    });
}

// Add custom CSS animations
function addCustomAnimations() {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideInRight {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        @keyframes slideOutRight {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
        
        @keyframes fadeInUp {
            from { transform: translateY(10px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        @keyframes fadeOutDown {
            from { transform: translateY(0); opacity: 1; }
            to { transform: translateY(10px); opacity: 0; }
        }
        
        .animate-in {
            animation: fadeInUp 0.6s ease-out forwards;
            opacity: 0;
            transform: translateY(30px);
        }
        
        .nav-menu.active {
            animation: slideInRight 0.3s ease-out;
        }
        
        .success-message {
            animation: fadeInUp 0.3s ease-out !important;
        }
        
        /* Smooth transitions for interactive elements */
        .cta-button, .menu-item, .contact-item, .social-link {
            transition: all 0.3s ease;
        }
        
        button, .cta-button {
            transition: transform 0.2s ease;
        }
    `;
    document.head.appendChild(style);
}

// Performance optimization
function optimizePerformance() {
    // Debounce scroll events
    let ticking = false;
    
    window.addEventListener('scroll', () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                // Scroll-related operations
                ticking = false;
            });
            ticking = true;
        }
    });
    
    // Preload critical resources
    const criticalImages = document.querySelectorAll('img[loading="lazy"]');
    criticalImages.forEach(img => {
        if (img.getBoundingClientRect().top < window.innerHeight * 2) {
            img.loading = 'eager';
        }
    });
    
    // Optimize animations for performance
    const animatedElements = document.querySelectorAll('.feature, .menu-item, .contact-item');
    animatedElements.forEach(el => {
        el.style.willChange = 'transform';
    });
    
    // Load non-critical resources after page load
    window.addEventListener('load', () => {
        // Lazy load non-critical resources here
        console.log('Page fully loaded - loading non-critical resources');
    });
}