// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    // Set initial viewport height for mobile browsers
    const vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
    
    // Initialize all functionality
    initializeNavigation();
    initializeAnimations();
    initializeDemo();
    initializeContactForm();
    initializeParticles();
});

// Navigation Functionality
function initializeNavigation() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');
    const navbar = document.querySelector('.navbar');

    // Mobile menu toggle
    hamburger.addEventListener('click', function() {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
        
        // Prevent body scroll when menu is open
        if (navMenu.classList.contains('active')) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }
    });

    // Close mobile menu when clicking outside
    document.addEventListener('click', function(e) {
        if (!navbar.contains(e.target) && navMenu.classList.contains('active')) {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
            document.body.style.overflow = '';
        }
    });

    // Close mobile menu when clicking on a link
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
            document.body.style.overflow = '';
        });
    });

    // Smooth scrolling for navigation links
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            
            if (targetSection) {
                // Account for navbar height
                const navbarHeight = navbar.offsetHeight;
                const targetPosition = targetSection.offsetTop - navbarHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Navbar background on scroll with throttling
    let ticking = false;
    function updateNavbar() {
        if (window.scrollY > 100) {
            navbar.style.background = 'rgba(10, 10, 10, 0.95)';
            navbar.style.backdropFilter = 'blur(25px)';
        } else {
            navbar.style.background = 'rgba(10, 10, 10, 0.9)';
            navbar.style.backdropFilter = 'blur(20px)';
        }
        ticking = false;
    }

    window.addEventListener('scroll', function() {
        if (!ticking) {
            requestAnimationFrame(updateNavbar);
            ticking = true;
        }
    });

    // Handle window resize
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
            document.body.style.overflow = '';
        }
    });
}

// Scroll to section function
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Animation on scroll
function initializeAnimations() {
    const fadeElements = document.querySelectorAll('.fade-in');
    
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    fadeElements.forEach(element => {
        observer.observe(element);
    });

    // Parallax effect for hero background
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const parallax = document.querySelector('.animated-bg');
        const speed = scrolled * 0.5;
        
        if (parallax) {
            parallax.style.transform = `translateY(${speed}px)`;
        }
    });
}

// Demo functionality
function initializeDemo() {
    const detectButton = document.getElementById('detect-btn');
    const textInput = document.getElementById('text-input');
    const resultDiv = document.getElementById('demo-result');

    // Sample responses for different types of text
    const responses = {
        positive: {
            level: 'Low Risk',
            color: '#00ff00',
            message: 'The text analysis indicates positive sentiment with no signs of depression. Mental health indicators appear stable.',
            confidence: '94%'
        },
        neutral: {
            level: 'Moderate Risk',
            color: '#ffaa00',
            message: 'The analysis shows mixed sentiment patterns. Some stress indicators detected but within normal ranges.',
            confidence: '87%'
        },
        negative: {
            level: 'High Risk',
            color: '#ff4444',
            message: 'The text analysis indicates potential signs of depression. Professional consultation is recommended.',
            confidence: '91%'
        }
    };

    detectButton.addEventListener('click', function() {
        const inputText = textInput.value.trim();
        
        if (!inputText) {
            showResult({
                level: 'No Input',
                color: '#666666',
                message: 'Please enter some text to analyze.',
                confidence: '0%'
            });
            return;
        }

        // Disable button and show loading
        detectButton.disabled = true;
        detectButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';

        // Simulate AI processing time
        setTimeout(() => {
            const result = analyzeText(inputText);
            showResult(result);
            
            // Re-enable button
            detectButton.disabled = false;
            detectButton.innerHTML = '<i class="fas fa-search"></i> Analyze Text';
        }, 2000);
    });

    function analyzeText(text) {
        const lowerText = text.toLowerCase();
        
        // Simple keyword-based analysis for demo purposes
        const negativeKeywords = ['sad', 'depressed', 'hopeless', 'worthless', 'empty', 'lonely', 'tired', 'anxious', 'worried', 'dark', 'pain', 'hurt', 'cry', 'death', 'suicide', 'hate myself'];
        const positiveKeywords = ['happy', 'joy', 'excited', 'love', 'grateful', 'blessed', 'amazing', 'wonderful', 'great', 'fantastic', 'awesome', 'perfect', 'smile', 'laugh'];
        
        let negativeScore = 0;
        let positiveScore = 0;
        
        negativeKeywords.forEach(keyword => {
            if (lowerText.includes(keyword)) {
                negativeScore++;
            }
        });
        
        positiveKeywords.forEach(keyword => {
            if (lowerText.includes(keyword)) {
                positiveScore++;
            }
        });
        
        if (negativeScore > positiveScore && negativeScore > 0) {
            return responses.negative;
        } else if (positiveScore > negativeScore) {
            return responses.positive;
        } else {
            return responses.neutral;
        }
    }

    function showResult(result) {
        resultDiv.innerHTML = `
            <div class="result-header">
                <h4>Analysis Result</h4>
                <div class="confidence-score" style="color: ${result.color}">
                    Confidence: ${result.confidence}
                </div>
            </div>
            <div class="result-content">
                <div class="risk-level" style="color: ${result.color}; font-weight: bold; font-size: 1.2rem; margin-bottom: 1rem;">
                    Risk Level: ${result.level}
                </div>
                <p>${result.message}</p>
                <div class="result-disclaimer" style="margin-top: 1rem; padding: 1rem; background: rgba(255, 255, 255, 0.05); border-radius: 8px; font-size: 0.9rem; color: #999;">
                    <strong>Disclaimer:</strong> This is a demonstration of AI text analysis. Results are simulated and should not be used for actual mental health assessment. Please consult with mental health professionals for real concerns.
                </div>
            </div>
        `;
        
        // Add animation to result
        resultDiv.style.opacity = '0';
        resultDiv.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            resultDiv.style.transition = 'all 0.5s ease';
            resultDiv.style.opacity = '1';
            resultDiv.style.transform = 'translateY(0)';
        }, 100);
    }
}

// Contact form functionality
function initializeContactForm() {
    const contactForm = document.getElementById('contact-form');
    const submitButton = contactForm.querySelector('.submit-button');

    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(contactForm);
        const name = formData.get('name');
        const email = formData.get('email');
        const message = formData.get('message');

        // Basic validation
        if (!name || !email || !message) {
            showNotification('Please fill in all fields.', 'error');
            return;
        }

        if (!isValidEmail(email)) {
            showNotification('Please enter a valid email address.', 'error');
            return;
        }

        // Simulate form submission
        submitButton.disabled = true;
        submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';

        setTimeout(() => {
            showNotification('Thank you for your message! We\'ll get back to you soon.', 'success');
            contactForm.reset();
            
            submitButton.disabled = false;
            submitButton.innerHTML = '<i class="fas fa-paper-plane"></i> Send Message';
        }, 2000);
    });

    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    function showNotification(message, type) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
                <span>${message}</span>
            </div>
        `;

        // Add styles
        notification.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            padding: 1rem 1.5rem;
            background: ${type === 'success' ? 'rgba(0, 255, 0, 0.1)' : 'rgba(255, 0, 0, 0.1)'};
            border: 1px solid ${type === 'success' ? '#00ff00' : '#ff0000'};
            border-radius: 10px;
            color: ${type === 'success' ? '#00ff00' : '#ff0000'};
            backdrop-filter: blur(10px);
            z-index: 1001;
            transform: translateX(100%);
            transition: transform 0.3s ease;
        `;

        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);

        // Remove after 5 seconds
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 5000);
    }
}

// Particle animation
function initializeParticles() {
    const particlesContainer = document.querySelector('.particles');
    
    // Adjust particle count based on screen size and device capabilities
    const getParticleCount = () => {
        const width = window.innerWidth;
        const isLowEnd = navigator.hardwareConcurrency <= 2 || navigator.deviceMemory <= 4;
        
        if (width < 480) return isLowEnd ? 15 : 25;
        if (width < 768) return isLowEnd ? 25 : 35;
        if (width < 1024) return isLowEnd ? 35 : 45;
        return isLowEnd ? 40 : 60;
    };

    // Check for reduced motion preference
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReducedMotion) {
        return; // Skip particle animation
    }

    let particleCount = getParticleCount();
    let particles = [];

    function createParticle() {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        const size = Math.random() * 3 + 1;
        const x = Math.random() * window.innerWidth;
        const y = Math.random() * window.innerHeight;
        const duration = Math.random() * 4 + 3;
        const delay = Math.random() * 2;
        const opacity = Math.random() * 0.5 + 0.3;

        particle.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            background: rgba(0, 255, 255, ${opacity});
            border-radius: 50%;
            left: ${x}px;
            top: ${y}px;
            animation: float ${duration}s ease-in-out infinite ${delay}s;
            pointer-events: none;
            will-change: transform;
        `;

        particlesContainer.appendChild(particle);
        particles.push(particle);

        // Remove and recreate particle after animation
        setTimeout(() => {
            if (particle.parentNode && particles.includes(particle)) {
                particle.parentNode.removeChild(particle);
                const index = particles.indexOf(particle);
                if (index > -1) particles.splice(index, 1);
                
                // Only recreate if we haven't exceeded the limit
                if (particles.length < particleCount) {
                    createParticle();
                }
            }
        }, (duration + delay) * 1000);
    }

    // Create initial particles
    for (let i = 0; i < particleCount; i++) {
        setTimeout(() => createParticle(), i * 100);
    }

    // Handle window resize
    let resizeTimeout;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            const newCount = getParticleCount();
            
            // Adjust particle count
            if (newCount < particles.length) {
                // Remove excess particles
                const excess = particles.length - newCount;
                for (let i = 0; i < excess; i++) {
                    if (particles[i] && particles[i].parentNode) {
                        particles[i].parentNode.removeChild(particles[i]);
                    }
                }
                particles = particles.slice(excess);
            } else if (newCount > particles.length) {
                // Add more particles
                const needed = newCount - particles.length;
                for (let i = 0; i < needed; i++) {
                    createParticle();
                }
            }
            
            particleCount = newCount;
            
            // Update existing particle positions
            particles.forEach(particle => {
                if (particle.parentNode) {
                    const x = Math.random() * window.innerWidth;
                    const y = Math.random() * window.innerHeight;
                    particle.style.left = x + 'px';
                    particle.style.top = y + 'px';
                }
            });
        }, 250);
    });
}

// Utility functions
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction() {
        const context = this;
        const args = arguments;
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

// Enhanced window resize handling
window.addEventListener('resize', debounce(function() {
    // Handle viewport height changes (mobile browsers)
    const vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
    
    // Recalculate hero section height for mobile
    const hero = document.querySelector('.hero');
    if (hero && window.innerWidth <= 768) {
        hero.style.height = `${window.innerHeight}px`;
    }
    
    // Update particle positions (handled in initializeParticles now)
    // Trigger scroll animations check
    const fadeElements = document.querySelectorAll('.fade-in');
    fadeElements.forEach(element => {
        const rect = element.getBoundingClientRect();
        const isVisible = rect.top < window.innerHeight && rect.bottom > 0;
        if (isVisible && !element.classList.contains('visible')) {
            element.classList.add('visible');
        }
    });
}, 250));

// Preload animations
window.addEventListener('load', function() {
    // Trigger initial animations
    const heroElements = document.querySelectorAll('.hero .fade-in');
    heroElements.forEach((element, index) => {
        setTimeout(() => {
            element.classList.add('visible');
        }, index * 200);
    });
});

// Add some interactive easter eggs
let konami = [];
const konamiCode = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65]; // Up, Up, Down, Down, Left, Right, Left, Right, B, A

document.addEventListener('keydown', function(e) {
    konami.push(e.keyCode);
    if (konami.length > konamiCode.length) {
        konami.shift();
    }
    
    if (konami.join(',') === konamiCode.join(',')) {
        // Easter egg: Enhanced visual effects
        document.body.style.filter = 'hue-rotate(180deg)';
        setTimeout(() => {
            document.body.style.filter = 'none';
        }, 3000);
        
        // Show secret message
        const message = document.createElement('div');
        message.innerHTML = '🧠 Secret AI Mode Activated! 🤖';
        message.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: var(--gradient-1);
            padding: 2rem;
            border-radius: 20px;
            font-family: 'Orbitron', monospace;
            font-size: 1.5rem;
            color: var(--dark-bg);
            z-index: 10000;
            animation: pulse 1s infinite;
        `;
        
        document.body.appendChild(message);
        
        setTimeout(() => {
            document.body.removeChild(message);
        }, 3000);
        
        konami = [];
    }
});

function openFullscreen(image) {
    const fullScreenDiv = document.createElement('div');
    fullScreenDiv.style.position = 'fixed';
    fullScreenDiv.style.top = '0';
    fullScreenDiv.style.left = '0';
    fullScreenDiv.style.width = '100%';
    fullScreenDiv.style.height = '100%';
    fullScreenDiv.style.backgroundColor = 'rgba(0, 0, 0, 0.9)';
    fullScreenDiv.style.display = 'flex';
    fullScreenDiv.style.justifyContent = 'center';
    fullScreenDiv.style.alignItems = 'center';
    fullScreenDiv.style.zIndex = '9999';

    const fullScreenImage = document.createElement('img');
    fullScreenImage.src = image.src;
    fullScreenImage.style.maxWidth = '90%';
    fullScreenImage.style.maxHeight = '90%';
    fullScreenImage.style.borderRadius = '8px';
    fullScreenImage.style.cursor = 'pointer'; // Makes the cursor a pointer

    const closeButton = document.createElement('span');
    closeButton.textContent = '×'; // Cross mark
    closeButton.style.position = 'absolute';
    closeButton.style.top = '20px';
    closeButton.style.right = '20px';
    closeButton.style.fontSize = '2rem';
    closeButton.style.color = '#fff';
    closeButton.style.cursor = 'pointer';
    closeButton.style.zIndex = '10000';

    closeButton.onclick = () => {
        document.body.removeChild(fullScreenDiv);
    };

    fullScreenDiv.appendChild(fullScreenImage);
    fullScreenDiv.appendChild(closeButton);

    document.body.appendChild(fullScreenDiv);
}
