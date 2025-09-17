// Mobile Optimization and Touch Enhancement
class MobileOptimizer {
    constructor() {
        this.isMobile = this.detectMobile();
        this.init();
    }
    
    detectMobile() {
        return window.innerWidth <= 768 || 
               navigator.userAgent.match(/Android/i) ||
               navigator.userAgent.match(/webOS/i) ||
               navigator.userAgent.match(/iPhone/i) ||
               navigator.userAgent.match(/iPad/i) ||
               navigator.userAgent.match(/iPod/i) ||
               navigator.userAgent.match(/BlackBerry/i) ||
               navigator.userAgent.match(/Windows Phone/i);
    }
    
    init() {
        this.optimizeTouchTargets();
        this.preventZoomOnDoubleTap();
        this.enhanceScrollPerformance();
        this.addViewportHeightFix();
    }
    
    optimizeTouchTargets() {
        // Ensure all interactive elements meet minimum touch target size
        const touchElements = document.querySelectorAll(
            'a, button, input, .cta-button, .newsletter-btn, .social-link'
        );
        
        touchElements.forEach(el => {
            if (this.isMobile) {
                el.style.minHeight = '44px';
                el.style.minWidth = '44px';
                el.style.display = 'flex';
                el.style.alignItems = 'center';
                el.style.justifyContent = 'center';
            }
        });
    }
    
    preventZoomOnDoubleTap() {
        // Prevent accidental zoom on double-tap
        let lastTouchEnd = 0;
        document.addEventListener('touchend', (event) => {
            const now = Date.now();
            if (now - lastTouchEnd <= 300) {
                event.preventDefault();
            }
            lastTouchEnd = now;
        }, { passive: false });
    }
    
    enhanceScrollPerformance() {
        // Add smooth scrolling for mobile
        document.addEventListener('touchstart', () => {
            document.body.style.overflow = 'hidden';
        }, { passive: true });
        
        document.addEventListener('touchend', () => {
            document.body.style.overflow = '';
        }, { passive: true });
    }
    
    addViewportHeightFix() {
        // Fix for mobile viewport height issues
        const setVh = () => {
            const vh = window.innerHeight * 0.01;
            document.documentElement.style.setProperty('--vh', `${vh}px`);
        };
        
        setVh();
        window.addEventListener('resize', setVh);
        window.addEventListener('orientationchange', setVh);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new MobileOptimizer();
});

// Add CSS custom property for viewport height fix
const style = document.createElement('style');
style.textContent = `
    #hero {
        min-height: calc(var(--vh, 1vh) * 80);
    }
    
    @media (max-width: 768px) {
        #hero {
            min-height: calc(var(--vh, 1vh) * 70);
        }
    }
    
    @media (max-width: 480px) {
        #hero {
            min-height: calc(var(--vh, 1vh) * 60);
        }
    }
`;
document.head.appendChild(style);