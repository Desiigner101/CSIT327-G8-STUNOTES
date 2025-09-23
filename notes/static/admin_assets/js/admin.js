// StuNotes Admin - Clean JavaScript Enhancement
document.addEventListener('DOMContentLoaded', function() {
    
    // Add smooth animations to dashboard modules
    function animateDashboard() {
        const modules = document.querySelectorAll('.dashboard .module');
        modules.forEach((module, index) => {
            module.style.opacity = '0';
            module.style.transform = 'translateY(20px)';
            module.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            
            setTimeout(() => {
                module.style.opacity = '1';
                module.style.transform = 'translateY(0)';
            }, index * 100);
        });
    }
    
    // Enhance search functionality
    function enhanceSearch() {
        const searchInput = document.querySelector('#searchbar');
        if (searchInput) {
            searchInput.addEventListener('focus', function() {
                this.style.borderColor = '#4f46e5';
                this.style.boxShadow = '0 0 0 3px rgba(79, 70, 229, 0.1)';
            });
            
            searchInput.addEventListener('blur', function() {
                if (!this.value) {
                    this.style.borderColor = '#e5e7eb';
                    this.style.boxShadow = 'none';
                }
            });
        }
    }
    
    // Add loading states to forms
    function addLoadingStates() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', function() {
                const submitBtn = form.querySelector('input[type="submit"], button[type="submit"]');
                if (submitBtn && !submitBtn.disabled) {
                    const originalText = submitBtn.value || submitBtn.textContent;
                    submitBtn.value = 'Saving...';
                    submitBtn.textContent = 'Saving...';
                    submitBtn.disabled = true;
                    submitBtn.style.opacity = '0.7';
                    
                    // Re-enable after a delay (in case of validation errors)
                    setTimeout(() => {
                        submitBtn.disabled = false;
                        submitBtn.value = originalText;
                        submitBtn.textContent = originalText;
                        submitBtn.style.opacity = '1';
                    }, 5000);
                }
            });
        });
    }
    
    // Enhance table interactions
    function enhanceTableRows() {
        const tableRows = document.querySelectorAll('#result_list tbody tr');
        tableRows.forEach(row => {
            row.addEventListener('mouseenter', function() {
                this.style.backgroundColor = '#f0f9ff';
                this.style.transition = 'background-color 0.2s ease';
            });
            
            row.addEventListener('mouseleave', function() {
                this.style.backgroundColor = '';
            });
        });
    }
    
    // Add status and priority indicators
    function addStatusIndicators() {
        // Add colored indicators for priority
        const cells = document.querySelectorAll('td');
        cells.forEach(cell => {
            const text = cell.textContent.trim().toLowerCase();
            
            if (text === 'high') {
                cell.innerHTML = '<span style="color: #ef4444; font-weight: 600;">🔴 High</span>';
            } else if (text === 'medium') {
                cell.innerHTML = '<span style="color: #f59e0b; font-weight: 600;">🟡 Medium</span>';
            } else if (text === 'low') {
                cell.innerHTML = '<span style="color: #10b981; font-weight: 600;">🟢 Low</span>';
            } else if (text === 'pending') {
                cell.innerHTML = '<span style="color: #f59e0b; font-weight: 600;">⏳ Pending</span>';
            } else if (text === 'completed') {
                cell.innerHTML = '<span style="color: #10b981; font-weight: 600;">✅ Completed</span>';
            } else if (text === 'in progress' || text === 'in_progress') {
                cell.innerHTML = '<span style="color: #06b6d4; font-weight: 600;">🔄 In Progress</span>';
            }
        });
    }
    
    // Enhance form fields
    function enhanceFormFields() {
        const formFields = document.querySelectorAll('input, textarea, select');
        formFields.forEach(field => {
            field.addEventListener('focus', function() {
                this.style.borderColor = '#4f46e5';
                this.style.boxShadow = '0 0 0 3px rgba(79, 70, 229, 0.1)';
                this.style.transition = 'border-color 0.2s ease, box-shadow 0.2s ease';
            });
            
            field.addEventListener('blur', function() {
                if (!this.value && this.required) {
                    this.style.borderColor = '#ef4444';
                    this.style.boxShadow = '0 0 0 3px rgba(239, 68, 68, 0.1)';
                } else {
                    this.style.borderColor = '#e5e7eb';
                    this.style.boxShadow = 'none';
                }
            });
        });
    }
    
    // Auto-hide success messages
    function handleMessages() {
        const messages = document.querySelectorAll('.messagelist li');
        messages.forEach((message, index) => {
            // Add close button
            const closeBtn = document.createElement('span');
            closeBtn.innerHTML = '×';
            closeBtn.style.cssText = `
                float: right;
                cursor: pointer;
                font-size: 1.2em;
                font-weight: bold;
                margin-left: 1rem;
                opacity: 0.8;
            `;
            closeBtn.addEventListener('click', () => {
                message.style.opacity = '0';
                message.style.transform = 'translateX(100%)';
                message.style.transition = 'all 0.3s ease';
                setTimeout(() => message.remove(), 300);
            });
            message.appendChild(closeBtn);
            
            // Auto-hide success messages after 5 seconds
            if (message.classList.contains('success') || message.textContent.includes('successfully')) {
                setTimeout(() => {
                    message.style.opacity = '0';
                    message.style.transform = 'translateX(100%)';
                    message.style.transition = 'all 0.3s ease';
                    setTimeout(() => message.remove(), 300);
                }, 5000);
            }
        });
    }
    
    // Add keyboard shortcuts
    function addKeyboardShortcuts() {
        document.addEventListener('keydown', function(e) {
            // Ctrl/Cmd + K to focus search
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                const searchInput = document.querySelector('#searchbar');
                if (searchInput) {
                    searchInput.focus();
                    searchInput.select();
                }
            }
            
            // Escape to clear search
            if (e.key === 'Escape') {
                const searchInput = document.querySelector('#searchbar');
                if (searchInput && document.activeElement === searchInput) {
                    searchInput.value = '';
                    searchInput.blur();
                }
            }
        });
    }
    
    // Add tooltips to action buttons
    function addTooltips() {
        const addButtons = document.querySelectorAll('.addlink');
        addButtons.forEach(btn => {
            btn.title = 'Add new item (Alt+A)';
        });
        
        const changeButtons = document.querySelectorAll('.changelink');
        changeButtons.forEach(btn => {
            btn.title = 'View and edit items';
        });
        
        const searchInput = document.querySelector('#searchbar');
        if (searchInput) {
            searchInput.placeholder = 'Search... (Ctrl+K)';
        }
    }
    
    // Add confirmation for delete actions
    function addDeleteConfirmation() {
        const deleteButtons = document.querySelectorAll('a[href*="delete/"]');
        deleteButtons.forEach(btn => {
            btn.addEventListener('click', function(e) {
                if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                    e.preventDefault();
                }
            });
        });
    }
    
    // Initialize all enhancements
    function init() {
        try {
            animateDashboard();
            enhanceSearch();
            addLoadingStates();
            enhanceTableRows();
            addStatusIndicators();
            enhanceFormFields();
            handleMessages();
            addKeyboardShortcuts();
            addTooltips();
            addDeleteConfirmation();
            
            console.log('StuNotes Admin Enhanced Successfully!');
        } catch (error) {
            console.log('Some enhancements could not be applied:', error);
        }
    }
    
    // Run initialization
    init();
    
    // Re-run some functions when navigating between admin pages
    window.addEventListener('popstate', function() {
        setTimeout(init, 100);
    });
});