document.addEventListener('DOMContentLoaded', function () {
    const header = document.querySelector('.site-header');
    const hamburgerMenu = document.querySelector('.hamburger-menu');
    const body = document.querySelector('body');

    if(header) {
        // Sticky header on scroll
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        
    // Careers Page Logic
    if (document.querySelector('.accordion')) {
        const accordionItems = document.querySelectorAll('.accordion-item');
        accordionItems.forEach(item => {
            const header = item.querySelector('.accordion-header');
            header.addEventListener('click', () => {
                const content = item.querySelector('.accordion-content');
                
                // Close other items
                accordionItems.forEach(otherItem => {
                    if (otherItem !== item && otherItem.classList.contains('active')) {
                        otherItem.classList.remove('active');
                        otherItem.querySelector('.accordion-content').style.maxHeight = '0px';
                        otherItem.querySelector('.accordion-icon').textContent = '+';
                    }
                
    // Contact Form Logic
    if (document.getElementById('contactForm')) {
        const form = document.getElementById('contactForm');
        const formStatus = document.getElementById('contactFormStatus');

        form.addEventListener('submit', function(event) {
            event.preventDefault();
            let isValid = validateContactForm();
            
            if (isValid) {
                form.style.display = 'none';
                formStatus.className = 'success';
                formStatus.textContent = 'Thank you for your message! We will get back to you soon.';
            } else {
                formStatus.className = 'error';
                formStatus.textContent = 'Please correct the errors before sending.';
            }
        });

        function validateContactForm() {
            let valid = true;
            const fields = ['contactName', 'contactEmail', 'contactCompany', 'department', 'message'];
            
            fields.forEach(id => {
                const input = document.getElementById(id);
                const errorContainer = input.parentElement.querySelector('.error-message');
                let message = '';

                if (input.required && !input.value.trim()) {
                    message = 'This field is required.';
                } else if (id === 'contactEmail' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value)) {
                    message = 'Please enter a valid email address.';
                }

                if (message) {
                    valid = false;
                    input.parentElement.classList.add('error');
                    errorContainer.textContent = message;
                } else {
                    input.parentElement.classList.remove('error');
                    errorContainer.textContent = '';
                }
            });

            return valid;
        }
    }
});

                // Toggle current item
                item.classList.toggle('active');
                if (item.classList.contains('active')) {
                    content.style.maxHeight = content.scrollHeight + 'px';
                    header.querySelector('.accordion-icon').textContent = '-';
                } else {
                    content.style.maxHeight = '0px';
                    header.querySelector('.accordion-icon').textContent = '+';
                }
            });
        });
    }

    if (document.getElementById('applicationForm')) {
        const form = document.getElementById('applicationForm');
        const formStatus = document.getElementById('formStatus');

        form.addEventListener('submit', function(event) {
            event.preventDefault();
            let isValid = validateForm();
            
            if (isValid) {
                form.style.display = 'none';
                formStatus.className = 'success';
                formStatus.textContent = 'Thank you for your application! We will be in touch shortly.';
            } else {
                formStatus.className = 'error';
                formStatus.textContent = 'Please correct the errors and try again.';
            }
        });

        function validateForm() {
            let valid = true;
            const fields = ['fullName', 'email', 'phone', 'resume'];
            
            fields.forEach(id => {
                const input = document.getElementById(id);
                const errorContainer = input.nextElementSibling;
                let message = '';

                if (input.required && !input.value.trim()) {
                    message = 'This field is required.';
                } else if (id === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value)) {
                    message = 'Please enter a valid email address.';
                } else if (id === 'resume' && input.files.length === 0) {
                    message = 'Please upload your resume.';
                }

                if (message) {
                    valid = false;
                    input.parentElement.classList.add('error');
                    errorContainer.textContent = message;
                } else {
                    input.parentElement.classList.remove('error');
                    errorContainer.textContent = '';
                }
            });

            return valid;
        }
    }
});
    }

    if(hamburgerMenu) {
        // Hamburger menu toggle
        hamburgerMenu.addEventListener('click', () => {
            body.classList.toggle('nav-open');
        });
    }

    // Fade-in animations
    const fadeInSections = document.querySelectorAll('.fade-in');
    if(fadeInSections.length > 0) {
        const sectionObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            rootMargin: '0px 0px -100px 0px'
        });

        fadeInSections.forEach(section => {
            sectionObserver.observe(section);
        });
    }

    // Case Studies Page Logic
    if (document.querySelector('.case-study-grid')) {
        const caseStudies = [
            { id: 1, title: 'AI-Driven Fraud Detection', clientIndustry: 'Finance', challenge: 'High rate of fraudulent transactions impacting revenue.', solution: 'Implemented a real-time machine learning model to detect and flag suspicious activities.', results: 'Reduced fraudulent transactions by 40%.', technologies: ['Python', 'TensorFlow', 'AWS'] },
            { id: 2, title: 'Predictive Patient Monitoring', clientIndustry: 'Healthcare', challenge: 'Needed to proactively identify at-risk patients in ICUs.', solution: 'Developed a predictive analytics tool that monitors vital signs and alerts staff to potential issues.', results: 'Improved patient outcomes by 25%.', technologies: ['R', 'Azure ML', 'SQL'] },
            { id: 3, title: 'Inventory Optimization System', clientIndustry: 'Retail', challenge: 'Struggled with overstocking and stockouts across multiple locations.', solution: 'Built an AI-powered system to forecast demand and optimize inventory levels.', results: 'Cut inventory holding costs by 15%.', technologies: ['Python', 'Scikit-learn', 'GCP'] },
            { id: 4, title: 'Automated Quality Control', clientIndustry: 'Manufacturing', challenge: 'Manual quality checks were slow and prone to human error.', solution: 'Deployed a computer vision system to automatically detect defects on the production line.', results: 'Increased defect detection rate by 98%.', technologies: ['C++', 'OpenCV', 'NVIDIA Jetson'] },
            { id: 5, title: 'Personalized Financial Advisory', clientIndustry: 'Finance', challenge: 'Difficulty in providing personalized advice to a large client base.', solution: 'Created a robo-advisor platform using NLP to understand client goals and suggest portfolios.', results: 'Increased client engagement by 30%.', technologies: ['Node.js', 'React', 'Dialogflow'] },
            { id: 6, title: 'Supply Chain Visibility', clientIndustry: 'Manufacturing', challenge: 'Lack of real-time visibility into the global supply chain.', solution: 'Built a centralized dashboard with predictive analytics for potential delays.', results: 'Reduced shipping delays by 20%.', technologies: ['Java', 'Kafka', 'Tableau'] }
        ];

        const grid = document.querySelector('.case-study-grid');
        const filters = document.querySelectorAll('.filter-btn');
        const modal = document.getElementById('caseStudyModal');
        const modalBody = document.getElementById('modalBody');
        const closeModalBtn = document.querySelector('.modal-close');

        function renderGrid(items) {
            grid.innerHTML = items.map(item => `
                <div class="cs-card" data-id="${item.id}" data-industry="${item.clientIndustry}">
                    <div class="cs-card-content">
                        <h3>${item.title}</h3>
                        <span class="industry-tag">${item.clientIndustry}</span>
                    </div>
                </div>
            `).join('');
        }

        function filterGrid() {
            const activeFilter = document.querySelector('.filter-btn.active').dataset.filter;
            const cards = document.querySelectorAll('.cs-card');
            
            cards.forEach(card => {
                const industry = card.dataset.industry;
                if (activeFilter === 'All' || industry === activeFilter) {
                    card.classList.remove('hidden');
                } else {
                    card.classList.add('hidden');
                }
            });
        }

        function openModal(id) {
            const caseStudy = caseStudies.find(cs => cs.id === parseInt(id));
            if (!caseStudy) return;

            modalBody.innerHTML = `
                <h2>${caseStudy.title}</h2>
                <p><strong>Industry:</strong> ${caseStudy.clientIndustry}</p>
                <h3>The Challenge</h3>
                <p>${caseStudy.challenge}</p>
                <h3>The Solution</h3>
                <p>${caseStudy.solution}</p>
                <h3>The Results</h3>
                <p>${caseStudy.results}</p>
                <h3>Technologies Used</h3>
                <div class="tech-tags">
                    ${caseStudy.technologies.map(tech => `<span class="tech-tag">${tech}</span>`).join('')}
                </div>
            `;
            modal.classList.add('visible');
        }

        function closeModal() {
            modal.classList.remove('visible');
        }

        filters.forEach(btn => {
            btn.addEventListener('click', () => {
                filters.forEach(f => f.classList.remove('active'));
                btn.classList.add('active');
                filterGrid();
            });
        });

        grid.addEventListener('click', (e) => {
            const card = e.target.closest('.cs-card');
            if (card) {
                openModal(card.dataset.id);
            }
        });

        closeModalBtn.addEventListener('click', closeModal);
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeModal();
            }
        });

        renderGrid(caseStudies);
    }
});


