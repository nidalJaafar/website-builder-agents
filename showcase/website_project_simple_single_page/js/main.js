document.addEventListener('DOMContentLoaded', () => {

    // --- Smooth Scrolling for Navigation Links ---
    const navLinks = document.querySelectorAll('nav a[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);

            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // --- Contact Form Handling ---
    const contactForm = document.getElementById('contact-form');
    const formStatus = document.getElementById('form-status');

    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            event.preventDefault();

            // Get form values
            const name = document.getElementById('name').value.trim();
            const email = document.getElementById('email').value.trim();
            const message = document.getElementById('message').value.trim();

            // Simple email validation regex
            const emailRegex = /^\\S+@\\S+\\.\\S+$/;

            // Validation logic
            if (name === '') {
                showStatusMessage('Please enter your name.', 'error');
                return;
            }
            if (email === '' || !emailRegex.test(email)) {
                showStatusMessage('Please enter a valid email address.', 'error');
                return;
            }
            if (message === '') {
                showStatusMessage('Please enter your message.', 'error');
                return;
            }

            // On success
            showStatusMessage('Thank you! Your message has been sent.', 'success');
            contactForm.reset();
        });
    }

    function showStatusMessage(message, type) {
        if (formStatus) {
            formStatus.textContent = message;
            if (type === 'success') {
                formStatus.style.color = 'green';
            } else if (type === 'error') {
                formStatus.style.color = 'red';
            }
        }
    }
});
