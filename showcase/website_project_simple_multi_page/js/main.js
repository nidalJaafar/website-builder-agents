document.addEventListener('DOMContentLoaded', () => {
    const contactForm = document.getElementById('contactForm');

    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const isValid = validateForm();

            if (isValid) {
                showSuccessMessage();
                contactForm.reset();
            }
        });
    }

    function validateForm() {
        let isValid = true;
        const name = document.getElementById('name');
        const email = document.getElementById('email');
        const message = document.getElementById('message');

        // Reset states
        clearError(name);
        clearError(email);
        clearError(message);

        // Validate Name
        if (name.value.trim() === '') {
            showError(name, 'Name is required.');
            isValid = false;
        }

        // Validate Email
        if (email.value.trim() === '') {
            showError(email, 'Email is required.');
            isValid = false;
        } else if (!isValidEmail(email.value.trim())) {
            showError(email, 'Please enter a valid email address.');
            isValid = false;
        }

        // Validate Message
        if (message.value.trim() === '') {
            showError(message, 'Message is required.');
            isValid = false;
        }

        return isValid;
    }

    function showError(input, message) {
        const formGroup = input.parentElement;
        const errorDisplay = formGroup.querySelector('.error-message');
        
        input.classList.add('error');
        errorDisplay.textContent = message;
        errorDisplay.style.display = 'block';
    }

    function clearError(input) {
        const formGroup = input.parentElement;
        const errorDisplay = formGroup.querySelector('.error-message');

        input.classList.remove('error');
        errorDisplay.textContent = '';
        errorDisplay.style.display = 'none';
    }

    function isValidEmail(email) {
        // A simple regex for email validation
        const regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return regex.test(email);
    }

    function showSuccessMessage() {
        const messageContainer = document.getElementById('form-message-container');
        messageContainer.innerHTML = '<div class="success-message">Thank you! Your message has been sent.</div>';
        
        setTimeout(() => {
            messageContainer.innerHTML = '';
        }, 5000); // Message disappears after 5 seconds
    }
});
