// home.js - Enhanced Dashboard JavaScript

document.addEventListener("DOMContentLoaded", function() {
    
    // ==================== Task Form Toggle ====================
    const toggleBtn = document.getElementById("toggleTaskForm");
    const taskForm = document.getElementById("taskForm");

    if (toggleBtn && taskForm) {
        toggleBtn.addEventListener("click", function() {
            if (taskForm.style.display === "none" || !taskForm.style.display) {
                taskForm.style.display = "block";
                toggleBtn.textContent = "✖ Close Form";
                toggleBtn.style.background = "linear-gradient(135deg, #f44336, #e57373)";
                
                // Smooth scroll to form
                taskForm.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            } else {
                taskForm.style.display = "none";
                toggleBtn.textContent = "+ Add Task";
                toggleBtn.style.background = "linear-gradient(135deg, #4caf50, #66bb6a)";
            }
        });
    }

    // ==================== Task Checkbox Completion ====================
    const taskCheckboxes = document.querySelectorAll('.task-list input[type="checkbox"]');
    
    taskCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const taskItem = this.closest('li');
            
            if (this.checked) {
                taskItem.style.opacity = '0.6';
                taskItem.style.textDecoration = 'line-through';
                
                // Add completion animation
                taskItem.style.transform = 'scale(0.98)';
                setTimeout(() => {
                    taskItem.style.transform = 'scale(1)';
                }, 200);
                
                // Show completion message
                showNotification('Task completed! 🎉', 'success');
            } else {
                taskItem.style.opacity = '1';
                taskItem.style.textDecoration = 'none';
            }
        });
        
        // Set initial state for checked items
        if (checkbox.checked) {
            const taskItem = checkbox.closest('li');
            taskItem.style.opacity = '0.6';
            taskItem.style.textDecoration = 'line-through';
        }
    });

    // ==================== Animated Stats Counter ====================
    function animateValue(element, start, end, duration) {
        if (!element) return;
        
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            const currentValue = Math.floor(progress * (end - start) + start);
            element.textContent = currentValue;
            
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }

    // Animate stat numbers on page load
    const statNumbers = document.querySelectorAll('.stat-number');
    statNumbers.forEach(stat => {
        const finalValue = parseInt(stat.textContent);
        stat.textContent = '0';
        animateValue(stat, 0, finalValue, 1500);
    });

    // ==================== Real-time Clock ====================
    function updateClock() {
        const now = new Date();
        const options = { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        };
        const dateString = now.toLocaleDateString('en-US', options);
        
        const clockElement = document.querySelector('.topbar-right p');
        if (clockElement) {
            clockElement.innerHTML = `Today is <strong>${dateString}</strong>`;
        }
    }
    
    updateClock();
    setInterval(updateClock, 60000); // Update every minute

    // ==================== Notification System ====================
    function showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Style the notification
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            background: ${type === 'success' ? '#4caf50' : type === 'error' ? '#f44336' : '#2196f3'};
            color: white;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            z-index: 9999;
            animation: slideInRight 0.3s ease;
            font-weight: 600;
        `;
        
        document.body.appendChild(notification);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    // Add animation keyframes
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideInRight {
            from {
                opacity: 0;
                transform: translateX(100px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        @keyframes slideOutRight {
            from {
                opacity: 1;
                transform: translateX(0);
            }
            to {
                opacity: 0;
                transform: translateX(100px);
            }
        }
    `;
    document.head.appendChild(style);

    // ==================== Delete Confirmation ====================
    const deleteButtons = document.querySelectorAll('.btn-danger');
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this task? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });

    // ==================== Smooth Scroll for Navigation ====================
    document.querySelectorAll('.sidebar nav a').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            // Add active state animation
            document.querySelectorAll('.sidebar nav a').forEach(link => {
                link.classList.remove('active');
            });
            this.classList.add('active');
        });
    });

    // ==================== Auto-save Form Data ====================
    const formInputs = document.querySelectorAll('.task-form input, .task-form textarea, .task-form select');
    
    formInputs.forEach(input => {
        input.addEventListener('input', function() {
            const formData = {};
            formInputs.forEach(field => {
                if (field.name) {
                    formData[field.name] = field.value;
                }
            });
            localStorage.setItem('taskFormDraft', JSON.stringify(formData));
        });
    });

    // Restore form data if available
    const savedFormData = localStorage.getItem('taskFormDraft');
    if (savedFormData) {
        const formData = JSON.parse(savedFormData);
        formInputs.forEach(input => {
            if (input.name && formData[input.name]) {
                input.value = formData[input.name];
            }
        });
    }

    // Clear draft on successful submit
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            localStorage.removeItem('taskFormDraft');
        });
    });

    // ==================== Task Priority Color Coding ====================
    function updateTaskColors() {
        const tasks = document.querySelectorAll('.task-list li');
        
        tasks.forEach(task => {
            const taskText = task.textContent.toLowerCase();
            
            if (taskText.includes('high')) {
                task.style.borderLeftColor = '#f44336';
                task.style.borderLeftWidth = '4px';
            } else if (taskText.includes('medium')) {
                task.style.borderLeftColor = '#ff9800';
                task.style.borderLeftWidth = '4px';
            } else if (taskText.includes('low')) {
                task.style.borderLeftColor = '#4caf50';
                task.style.borderLeftWidth = '4px';
            }
        });
    }
    
    updateTaskColors();

    // ==================== Dynamic Progress Bar ====================
    function updateProgressBar() {
        const totalTasks = document.querySelectorAll('.task-list li').length;
        const completedTasks = document.querySelectorAll('.task-list input[type="checkbox"]:checked').length;
        
        if (totalTasks > 0) {
            const percentage = (completedTasks / totalTasks) * 100;
            
            // Update stats if element exists
            const progressText = document.querySelector('.progress-text');
            if (progressText) {
                progressText.textContent = `${completedTasks} of ${totalTasks} tasks completed (${Math.round(percentage)}%)`;
            }
        }
    }
    
    updateProgressBar();
    
    // Update progress when checkbox changes
    taskCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateProgressBar);
    });

    // ==================== Note Hover Effects ====================
    const notes = document.querySelectorAll('.note');
    notes.forEach(note => {
        note.addEventListener('mouseenter', function() {
            this.style.borderLeftWidth = '6px';
        });
        
        note.addEventListener('mouseleave', function() {
            this.style.borderLeftWidth = '4px';
        });
    });

    // ==================== Calendar Today Highlight ====================
    const today = new Date().getDate();
    const calendarCells = document.querySelectorAll('.calendar-box td');
    
    calendarCells.forEach(cell => {
        if (parseInt(cell.textContent) === today) {
            cell.classList.add('today');
        }
    });

    // ==================== Sidebar Stats Animation ====================
    const sidebarStats = document.querySelectorAll('.sidebar .stats span');
    sidebarStats.forEach(stat => {
        const finalValue = parseInt(stat.textContent);
        stat.textContent = '0';
        animateValue(stat, 0, finalValue, 2000);
    });

    // ==================== Task Due Date Warning ====================
    function checkDueDates() {
        const tasks = document.querySelectorAll('.task-list li');
        const now = new Date();
        
        tasks.forEach(task => {
            const dueDateText = task.querySelector('small');
            if (dueDateText) {
                const dateMatch = dueDateText.textContent.match(/Due: (.+?) \|/);
                if (dateMatch) {
                    const dueDate = new Date(dateMatch[1]);
                    const hoursDiff = (dueDate - now) / (1000 * 60 * 60);
                    
                    if (hoursDiff < 24 && hoursDiff > 0) {
                        task.style.background = 'linear-gradient(135deg, #fff3cd 0%, #ffffff 100%)';
                        task.style.borderLeftColor = '#ff9800';
                    } else if (hoursDiff < 0) {
                        task.style.background = 'linear-gradient(135deg, #ffebee 0%, #ffffff 100%)';
                        task.style.borderLeftColor = '#f44336';
                    }
                }
            }
        });
    }
    
    checkDueDates();

    // ==================== Welcome Message ====================
    const userName = document.querySelector('.topbar-left h2').textContent.replace('Welcome, ', '');
    const hour = new Date().getHours();
    let greeting = '';
    
    if (hour < 12) greeting = 'Good morning';
    else if (hour < 18) greeting = 'Good afternoon';
    else greeting = 'Good evening';
    
    document.querySelector('.topbar-left h2').textContent = `${greeting}, ${userName}!`;

    // ==================== Keyboard Shortcuts ====================
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + N: New Task
        if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
            e.preventDefault();
            if (toggleBtn) toggleBtn.click();
        }
        
        // ESC: Close task form
        if (e.key === 'Escape' && taskForm && taskForm.style.display === 'block') {
            toggleBtn.click();
        }
    });

    console.log('✅ StuNotes Dashboard Enhanced!');
    console.log('💡 Keyboard shortcuts:');
    console.log('   - Ctrl/Cmd + N: Add new task');
    console.log('   - ESC: Close task form');
});