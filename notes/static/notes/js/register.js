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
  const leftPanel = document.querySelector('.left-panel');
  const rightPanel = document.querySelector('.right-panel');
  const logo = document.querySelector('.logo-container');
  const formTitle = document.querySelector('.form-container h2');
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

// Smooth page transition when clicking sign in link
const signInLink = document.querySelector('.create-now');
if (signInLink) {
  signInLink.addEventListener('click', function(e) {
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

// Password toggle functionality
function togglePassword(fieldId) {
  const field = document.getElementById(fieldId);
  const button = field.nextElementSibling;
  
  if (field.type === 'password') {
    field.type = 'text';
    button.innerHTML = `
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
        <line x1="1" y1="1" x2="23" y2="23"/>
      </svg>
    `;
  } else {
    field.type = 'password';
    button.innerHTML = `
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
        <circle cx="12" cy="12" r="3"/>
      </svg>
    `;
  }
}

// Add transition to toggle buttons
const toggleButtons = document.querySelectorAll('.toggle-password');
toggleButtons.forEach(btn => {
  btn.style.transition = 'transform 0.2s ease';
});

// Make togglePassword globally available
window.togglePassword = togglePassword;

// Form validation
const registerForm = document.querySelector('form');
const fullNameInput = document.querySelector('#full_name');
const emailInput = document.querySelector('#email');
const password1Input = document.querySelector('#password1');
const password2Input = document.querySelector('#password2');
const submitBtn = document.querySelector('.submit-btn');

if (registerForm) {
  registerForm.addEventListener('submit', function(e) {
    let isValid = true;
    
    // Clear previous error styles
    clearErrors();
    
    // Validate full name
    if (!fullNameInput.value.trim()) {
      showError(fullNameInput, 'Full name is required');
      isValid = false;
    } else if (fullNameInput.value.trim().length < 2) {
      showError(fullNameInput, 'Full name must be at least 2 characters');
      isValid = false;
    }
    
    // Validate email
    if (!emailInput.value.trim()) {
      showError(emailInput, 'Email is required');
      isValid = false;
    } else if (!isValidEmail(emailInput.value)) {
      showError(emailInput, 'Please enter a valid email address');
      isValid = false;
    }
    
    // Validate password
    if (!password1Input.value.trim()) {
      showError(password1Input, 'Password is required');
      isValid = false;
    } else if (password1Input.value.length < 8) {
      showError(password1Input, 'Password must be at least 8 characters');
      isValid = false;
    } else if (!isStrongPassword(password1Input.value)) {
      showError(password1Input, 'Password must contain uppercase, lowercase, and number');
      isValid = false;
    }
    
    // Validate confirm password
    if (!password2Input.value.trim()) {
      showError(password2Input, 'Please confirm your password');
      isValid = false;
    } else if (password1Input.value !== password2Input.value) {
      showError(password2Input, 'Passwords do not match');
      isValid = false;
    }
    
    // Prevent form submission if validation fails
    if (!isValid) {
      e.preventDefault();
      return;
    }
  });
}

// Email validation helper
function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

// Strong password validation
function isStrongPassword(password) {
  const hasUpperCase = /[A-Z]/.test(password);
  const hasLowerCase = /[a-z]/.test(password);
  const hasNumber = /[0-9]/.test(password);
  return hasUpperCase && hasLowerCase && hasNumber;
}

// Show error message
function showError(input, message) {
  const inputWrapper = input.closest('.input-wrapper') || input.parentElement;
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
if (fullNameInput) {
  fullNameInput.addEventListener('input', function() {
    if (this.value.trim() !== '') {
      const errorMsg = this.closest('.form-group').querySelector('.error-message');
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

if (emailInput) {
  emailInput.addEventListener('input', function() {
    if (this.value.trim() !== '') {
      const errorMsg = this.closest('.form-group').querySelector('.error-message');
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

if (password1Input) {
  password1Input.addEventListener('input', function() {
    if (this.value.trim() !== '') {
      const errorMsg = this.closest('.form-group').querySelector('.error-message');
      if (errorMsg) {
        errorMsg.style.transition = 'opacity 0.3s ease';
        errorMsg.style.opacity = '0';
        setTimeout(() => {
          errorMsg.remove();
          this.style.borderColor = '#d1d5db';
        }, 300);
      }
    }
    
    // Update password strength indicator
    updatePasswordStrength(this.value);
  });
}

if (password2Input) {
  password2Input.addEventListener('input', function() {
    if (this.value.trim() !== '') {
      const errorMsg = this.closest('.form-group').querySelector('.error-message');
      if (errorMsg) {
        errorMsg.style.transition = 'opacity 0.3s ease';
        errorMsg.style.opacity = '0';
        setTimeout(() => {
          errorMsg.remove();
          this.style.borderColor = '#d1d5db';
        }, 300);
      }
    }
    
    // Check if passwords match with animation
    if (password1Input.value && this.value === password1Input.value) {
      this.style.transition = 'border-color 0.3s ease';
      this.style.borderColor = '#10b981';
    }
  });
}

// Password strength indicator (reuses element instead of duplicating)
function updatePasswordStrength(password) {
  let strength = 0;
  
  if (password.length >= 8) strength++;
  if (password.length >= 12) strength++;
  if (/[a-z]/.test(password)) strength++;
  if (/[A-Z]/.test(password)) strength++;
  if (/[0-9]/.test(password)) strength++;
  if (/[^a-zA-Z0-9]/.test(password)) strength++;
  
  let indicator = password1Input.closest('.form-group').querySelector('.password-strength');
  
  if (!indicator) {
    indicator = document.createElement('div');
    indicator.className = 'password-strength';
    indicator.style.marginTop = '0.5rem';
    indicator.style.fontSize = '0.875rem';
    password1Input.closest('.form-group').appendChild(indicator);
  }
  
  let color, text;
  if (strength <= 2) {
    color = '#dc2626';
    text = 'Weak';
  } else if (strength <= 4) {
    color = '#f59e0b';
    text = 'Medium';
  } else {
    color = '#10b981';
    text = 'Strong';
  }
  
  if (password.length > 0) {
    indicator.innerHTML = `
      <div style="display: flex; align-items: center; gap: 0.5rem; opacity: 1; transition: opacity 0.3s ease;">
        <div style="flex: 1; height: 4px; background: #e5e7eb; border-radius: 2px; overflow: hidden;">
          <div style="height: 100%; width: ${(strength / 6) * 100}%; background: ${color}; transition: all 0.5s ease;"></div>
        </div>
        <span style="color: ${color}; font-weight: 600;">${text}</span>
      </div>
    `;
  } else {
    indicator.innerHTML = '';
  }
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
  // Press Ctrl/Cmd + Enter to submit form
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
    if (registerForm) {
      registerForm.requestSubmit();
    }
  }
});

// Add smooth focus transitions
const inputs = document.querySelectorAll('.form-group input');
inputs.forEach(input => {
  input.addEventListener('focus', function() {
    this.closest('.form-group').style.transform = 'scale(1.02)';
    this.closest('.form-group').style.transition = 'transform 0.2s ease';
  });
  
  input.addEventListener('blur', function() {
    this.closest('.form-group').style.transform = 'scale(1)';
  });
});

// Prevent multiple form submissions
let isSubmitting = false;
if (registerForm) {
  registerForm.addEventListener('submit', function(e) {
    if (isSubmitting) {
      e.preventDefault();
      return false;
    }
    isSubmitting = true;
  });
}

// Auto-fill suggestion for email domain
if (emailInput) {
  emailInput.addEventListener('input', function(e) {
    const value = this.value;
    if (value.includes('@') && !value.includes('.')) {
      const commonDomains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com'];
      // Could add auto-suggestion dropdown here if desired
    }
  });
}

console.log('✅ Register page JavaScript loaded successfully');