// Page transition on load
document.addEventListener('DOMContentLoaded', function() {
  // Fade in animation on page load
  document.body.style.opacity = '0';
  document.body.style.transition = 'opacity 0.5s ease';
  
  setTimeout(() => {
    document.body.style.opacity = '1';
  }, 10);
  
  // Animate elements individually
  animateElements();
});

// Animate elements on page load
function animateElements() {
  const leftPanel = document.querySelector('.left-side');
  const rightPanel = document.querySelector('.right-side');
  const logo = document.querySelector('.logo-container');
  const formTitle = document.querySelector('.form-title');
  const formGroups = document.querySelectorAll('.form-group');
  const submitBtn = document.querySelector('.submit-btn');
  
  if (leftPanel) {
    leftPanel.style.opacity = '0';
    leftPanel.style.transform = 'translateX(-30px)';
    leftPanel.style.transition = 'all 0.6s ease';
    setTimeout(() => {
      leftPanel.style.opacity = '1';
      leftPanel.style.transform = 'translateX(0)';
    }, 100);
  }
  
  if (rightPanel) {
    rightPanel.style.opacity = '0';
    rightPanel.style.transform = 'translateX(30px)';
    rightPanel.style.transition = 'all 0.6s ease';
    setTimeout(() => {
      rightPanel.style.opacity = '1';
      rightPanel.style.transform = 'translateX(0)';
    }, 200);
  }
  
  const elements = [logo, formTitle, ...formGroups, submitBtn];
  elements.forEach((el, index) => {
    if (el) {
      el.style.opacity = '0';
      el.style.transform = 'translateY(20px)';
      el.style.transition = 'all 0.5s ease';
      setTimeout(() => {
        el.style.opacity = '1';
        el.style.transform = 'translateY(0)';
      }, 300 + (index * 80));
    }
  });
}

// Smooth page transition when clicking sign up link
const signUpLink = document.querySelector('.create-now');
if (signUpLink) {
  signUpLink.addEventListener('click', function(e) {
    e.preventDefault();
    const href = this.getAttribute('href');
    
    // Fade out animation
    document.body.style.transition = 'opacity 0.4s ease';
    document.body.style.opacity = '0';
    
    // Navigate after animation
    setTimeout(() => {
      window.location.href = href;
    }, 400);
  });
}

// Auto dismiss alert messages after 3 seconds
function autoDismissAlerts() {
  setTimeout(function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
      alert.style.transition = "opacity 0.5s ease";
      alert.style.opacity = "0";
      setTimeout(() => alert.remove(), 500);
    });
  }, 3000);
}

// Initialize alerts on page load
autoDismissAlerts();

// Form validation
const loginForm = document.querySelector('form');
const emailInput = document.querySelector('#email');
const passwordInput = document.querySelector('#password');

if (loginForm) {
  loginForm.addEventListener('submit', function(e) {
    let isValid = true;
    
    // Clear previous error styles
    clearErrors();
    
    // Validate email
    if (!emailInput.value.trim()) {
      showError(emailInput, 'Email is required');
      isValid = false;
    } else if (!isValidEmail(emailInput.value)) {
      showError(emailInput, 'Please enter a valid email address');
      isValid = false;
    }
    
    // Validate password
    if (!passwordInput.value.trim()) {
      showError(passwordInput, 'Password is required');
      isValid = false;
    } else if (passwordInput.value.length < 6) {
      showError(passwordInput, 'Password must be at least 6 characters');
      isValid = false;
    }
    
    // Prevent form submission if validation fails
    if (!isValid) {
      e.preventDefault();
    }
  });
}

// Email validation helper
function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

// Show error message
function showError(input, message) {
  const formGroup = input.closest('.form-group');
  const errorDiv = document.createElement('div');
  errorDiv.className = 'error-message';
  errorDiv.textContent = message;
  errorDiv.style.color = '#dc2626';
  errorDiv.style.fontSize = '0.875rem';
  errorDiv.style.marginTop = '0.25rem';
  errorDiv.style.animation = 'slideIn 0.3s ease';
  
  input.style.borderColor = '#dc2626';
  formGroup.appendChild(errorDiv);
  
  // Add animation keyframes
  if (!document.querySelector('#errorAnimation')) {
    const style = document.createElement('style');
    style.id = 'errorAnimation';
    style.textContent = `
      @keyframes slideIn {
        from {
          opacity: 0;
          transform: translateY(-10px);
        }
        to {
          opacity: 1;
          transform: translateY(0);
        }
      }
    `;
    document.head.appendChild(style);
  }
}

// Clear all error messages
function clearErrors() {
  const errorMessages = document.querySelectorAll('.error-message');
  errorMessages.forEach(error => error.remove());
  
  const inputs = document.querySelectorAll('.form-group input');
  inputs.forEach(input => {
    input.style.borderColor = '#d1d5db';
  });
}

// Real-time validation on input
if (emailInput) {
  emailInput.addEventListener('input', function() {
    if (this.value.trim() !== '') {
      const errorMsg = this.parentElement.querySelector('.error-message');
      if (errorMsg) {
        errorMsg.style.transition = 'opacity 0.3s ease';
        errorMsg.style.opacity = '0';
        setTimeout(() => {
          errorMsg.remove();
          this.style.borderColor = '#d1d5db';
        }, 300);
      }
    }
  });
}

if (passwordInput) {
  passwordInput.addEventListener('input', function() {
    if (this.value.trim() !== '') {
      const errorMsg = this.parentElement.querySelector('.error-message');
      if (errorMsg) {
        errorMsg.style.transition = 'opacity 0.3s ease';
        errorMsg.style.opacity = '0';
        setTimeout(() => {
          errorMsg.remove();
          this.style.borderColor = '#d1d5db';
        }, 300);
      }
    }
  });
}

// Remember me functionality
const rememberMeCheckbox = document.querySelector('#remember');
if (rememberMeCheckbox && emailInput) {
  // Load saved email on page load
  const savedEmail = localStorage.getItem('rememberedEmail');
  if (savedEmail) {
    emailInput.value = savedEmail;
    rememberMeCheckbox.checked = true;
  }
  
  // Save email when form is submitted
  if (loginForm) {
    loginForm.addEventListener('submit', function() {
      if (rememberMeCheckbox.checked) {
        localStorage.setItem('rememberedEmail', emailInput.value);
      } else {
        localStorage.removeItem('rememberedEmail');
      }
    });
  }
}

// Loading state for submit button
const submitBtn = document.querySelector('.submit-btn');
if (submitBtn && loginForm) {
  loginForm.addEventListener('submit', function() {
    if (loginForm.checkValidity()) {
      submitBtn.disabled = true;
      submitBtn.style.opacity = '0.7';
      submitBtn.style.cursor = 'not-allowed';
      
      const originalText = submitBtn.textContent;
      submitBtn.innerHTML = '<span style="display: inline-flex; align-items: center; gap: 0.5rem;">Processing... <span class="spinner"></span></span>';
      
      // Add spinner styles
      const style = document.createElement('style');
      style.textContent = `
        .spinner {
          width: 16px;
          height: 16px;
          border: 2px solid rgba(255, 255, 255, 0.3);
          border-top-color: white;
          border-radius: 50%;
          animation: spin 0.8s linear infinite;
        }
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
      `;
      document.head.appendChild(style);
    }
  });
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
  // Press Ctrl/Cmd + Enter to submit form
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
    if (loginForm) {
      loginForm.requestSubmit();
    }
  }
});

// Add smooth focus transitions
const inputs = document.querySelectorAll('.form-group input');
inputs.forEach(input => {
  input.addEventListener('focus', function() {
    this.parentElement.style.transform = 'scale(1.02)';
    this.parentElement.style.transition = 'transform 0.2s ease';
  });
  
  input.addEventListener('blur', function() {
    this.parentElement.style.transform = 'scale(1)';
  });
});

// Prevent multiple form submissions
let isSubmitting = false;
if (loginForm) {
  loginForm.addEventListener('submit', function(e) {
    if (isSubmitting) {
      e.preventDefault();
      return false;
    }
    isSubmitting = true;
  });
}
