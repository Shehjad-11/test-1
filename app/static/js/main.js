// Modern JavaScript for CollabPlatform

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeComponents();
    
    // Load notification count
    loadNotificationCount();
    
    // Refresh notification count every 30 seconds
    setInterval(loadNotificationCount, 30000);
    
    // Initialize animations
    initializeAnimations();
    
    // Initialize form enhancements
    initializeFormEnhancements();
    
    // Initialize project features
    initializeProjectFeatures();
});

function initializeComponents() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
}

function initializeAnimations() {
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements for animation
    document.querySelectorAll('.card, .hero-content').forEach(el => {
        observer.observe(el);
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

function initializeFormEnhancements() {
    // Enhanced form validation
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Focus on first invalid field
                const firstInvalid = form.querySelector(':invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                    firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Real-time validation feedback
    document.querySelectorAll('.form-control, .form-select').forEach(input => {
        input.addEventListener('blur', function() {
            if (this.checkValidity()) {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            } else {
                this.classList.remove('is-valid');
                this.classList.add('is-invalid');
            }
        });

        input.addEventListener('input', function() {
            if (this.classList.contains('is-invalid') && this.checkValidity()) {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            }
        });
    });

    // Skills input enhancement
    initializeSkillsInput();
}

function initializeProjectFeatures() {
    // Project deadline countdowns
    initializeCountdowns();
    
    // Project card interactions
    document.querySelectorAll('.card-project').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Load unread notification count
function loadNotificationCount() {
    fetch('/api/notifications/unread-count')
        .then(response => response.json())
        .then(data => {
            const badge = document.getElementById('notification-badge');
            if (badge) {
                if (data.count > 0) {
                    badge.textContent = data.count > 99 ? '99+' : data.count;
                    badge.style.display = 'flex';
                    
                    // Add pulse animation for new notifications
                    badge.style.animation = 'pulse 2s infinite';
                } else {
                    badge.style.display = 'none';
                    badge.style.animation = 'none';
                }
            }
        })
        .catch(error => console.error('Error loading notification count:', error));
}

// Mark notification as read
function markNotificationRead(notificationId) {
    fetch(`/api/notifications/mark-read/${notificationId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            loadNotificationCount();
            
            // Update notification item visually
            const notificationItem = document.querySelector(`[data-notification-id="${notificationId}"]`);
            if (notificationItem) {
                notificationItem.classList.add('opacity-50');
            }
        }
    })
    .catch(error => console.error('Error marking notification as read:', error));
}

// Project deadline countdowns
function initializeCountdowns() {
    const countdownElements = document.querySelectorAll('[data-countdown]');
    
    countdownElements.forEach(function(element) {
        const deadline = new Date(element.dataset.countdown);
        updateCountdown(element, deadline);
        
        // Update every minute
        setInterval(function() {
            updateCountdown(element, deadline);
        }, 60000);
    });
}

function updateCountdown(element, deadline) {
    const now = new Date();
    const timeLeft = deadline - now;
    
    if (timeLeft <= 0) {
        element.textContent = 'Expired';
        element.className = 'badge bg-danger';
        return;
    }
    
    const days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
    const hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
    
    let displayText = '';
    let badgeClass = 'badge ';
    
    if (days > 0) {
        displayText = `${days}d ${hours}h`;
    } else if (hours > 0) {
        displayText = `${hours}h ${minutes}m`;
    } else {
        displayText = `${minutes}m`;
    }
    
    // Color coding based on time left
    if (days < 1) {
        badgeClass += 'bg-danger';
    } else if (days < 3) {
        badgeClass += 'bg-warning';
    } else {
        badgeClass += 'bg-success';
    }
    
    element.textContent = displayText;
    element.className = badgeClass;
}

// Skills input enhancement
function initializeSkillsInput() {
    const skillsInputs = document.querySelectorAll('textarea[name*="skills"], input[name*="skills"]');
    
    skillsInputs.forEach(function(input) {
        // Add skill suggestions
        const suggestedSkills = [
            'JavaScript', 'Python', 'React', 'Node.js', 'HTML', 'CSS', 'TypeScript',
            'Vue.js', 'Angular', 'Django', 'Flask', 'PostgreSQL', 'MongoDB',
            'UI/UX Design', 'Figma', 'Adobe Creative Suite', 'Sketch', 'Prototyping',
            'Mobile Design', 'Web Design', 'Graphic Design', 'Branding'
        ];
        
        // Create suggestions container
        const suggestionsContainer = document.createElement('div');
        suggestionsContainer.className = 'skills-suggestions mt-2';
        suggestionsContainer.innerHTML = '<small class="text-muted">Popular skills:</small><br>';
        
        suggestedSkills.slice(0, 8).forEach(skill => {
            const skillBadge = document.createElement('span');
            skillBadge.className = 'badge bg-light text-dark me-1 mb-1 cursor-pointer';
            skillBadge.textContent = skill;
            skillBadge.style.cursor = 'pointer';
            
            skillBadge.addEventListener('click', function() {
                const currentSkills = input.value.split(',').map(s => s.trim()).filter(s => s);
                if (!currentSkills.includes(skill)) {
                    currentSkills.push(skill);
                    input.value = currentSkills.join(', ');
                    input.dispatchEvent(new Event('input'));
                }
            });
            
            suggestionsContainer.appendChild(skillBadge);
        });
        
        input.parentNode.appendChild(suggestionsContainer);
        
        // Clean up skills format on blur
        input.addEventListener('blur', function() {
            const skills = input.value.split(',').map(s => s.trim()).filter(s => s);
            input.value = skills.join(', ');
        });
    });
}

// Utility functions
function showLoading(element) {
    element.classList.add('loading');
    element.disabled = true;
    const originalText = element.textContent;
    element.textContent = 'Loading...';
    element.dataset.originalText = originalText;
}

function hideLoading(element) {
    element.classList.remove('loading');
    element.disabled = false;
    if (element.dataset.originalText) {
        element.textContent = element.dataset.originalText;
        delete element.dataset.originalText;
    }
}

// Confirm actions with modern modal
function confirmAction(message, title = 'Confirm Action') {
    return new Promise((resolve) => {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${title}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <p>${message}</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-danger" id="confirm-action">Confirm</button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        const bsModal = new bootstrap.Modal(modal);
        
        modal.querySelector('#confirm-action').addEventListener('click', () => {
            bsModal.hide();
            resolve(true);
        });
        
        modal.addEventListener('hidden.bs.modal', () => {
            document.body.removeChild(modal);
            resolve(false);
        });
        
        bsModal.show();
    });
}

// Copy to clipboard with feedback
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showToast('Copied to clipboard!', 'success');
    }).catch(function(err) {
        console.error('Could not copy text: ', err);
        showToast('Failed to copy to clipboard', 'error');
    });
}

// Enhanced toast notifications
function showToast(message, type = 'info', duration = 3000) {
    const toastContainer = document.getElementById('toast-container') || createToastContainer();
    
    const toastId = 'toast-' + Date.now();
    const iconMap = {
        success: 'check-circle',
        error: 'x-circle',
        warning: 'exclamation-triangle',
        info: 'info-circle'
    };
    
    const toast = document.createElement('div');
    toast.id = toastId;
    toast.className = `toast align-items-center text-white bg-${type === 'error' ? 'danger' : type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="bi bi-${iconMap[type] || 'info-circle'} me-2"></i>
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast, { delay: duration });
    bsToast.show();
    
    // Remove toast element after it's hidden
    toast.addEventListener('hidden.bs.toast', function() {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    container.style.zIndex = '1055';
    document.body.appendChild(container);
    return container;
}

// Search functionality
function initializeSearch() {
    const searchInputs = document.querySelectorAll('[data-search]');
    
    searchInputs.forEach(input => {
        let searchTimeout;
        
        input.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.toLowerCase();
            const target = this.dataset.search;
            
            searchTimeout = setTimeout(() => {
                const items = document.querySelectorAll(target);
                
                items.forEach(item => {
                    const text = item.textContent.toLowerCase();
                    if (text.includes(query) || query === '') {
                        item.style.display = '';
                        item.classList.add('fade-in');
                    } else {
                        item.style.display = 'none';
                        item.classList.remove('fade-in');
                    }
                });
            }, 300);
        });
    });
}

// Initialize search on page load
document.addEventListener('DOMContentLoaded', initializeSearch);

// Add CSS for pulse animation
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    .cursor-pointer {
        cursor: pointer;
    }
    
    .skills-suggestions .badge:hover {
        background-color: var(--primary-color) !important;
        color: white !important;
        transform: translateY(-1px);
    }
`;
document.head.appendChild(style);