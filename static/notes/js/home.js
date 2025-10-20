// ==================== Modal Functions ====================
function openModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

window.openModal = openModal;
window.closeModal = closeModal;

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

    // ==================== Task Completion Animation ====================
    document.querySelectorAll('.btn-complete').forEach(button => {
        button.addEventListener('click', function(e) {
            const taskItem = this.closest('li');
            
            // Add completion animation
            taskItem.style.transform = 'scale(0.95)';
            taskItem.style.opacity = '0.7';
            
            setTimeout(() => {
                taskItem.style.transform = 'scale(1)';
                taskItem.style.opacity = '1';
            }, 200);
        });
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
        if (!isNaN(finalValue)) {
            stat.textContent = '0';
            animateValue(stat, 0, finalValue, 1500);
        }
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
    const deleteButtons = document.querySelectorAll('.btn-delete');
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
        const textContent = stat.textContent.trim();
        const finalValue = parseInt(textContent);
        
        // Only animate if it's a valid number
        if (!isNaN(finalValue)) {
            stat.textContent = '0';
            animateValue(stat, 0, finalValue, 2000);
        }
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

    // ==================== Modal Functions ====================
    function openCompletedTasksModal() {
        openModal('completedTasksModal');
    }

    function openPendingTasksModal() {
        openModal('pendingTasksModal');
    }

    function openOverdueTasksModal() {
        openModal('overdueTasksModal');
    }

    function openAllNotesModal() {
        openModal('allNotesModal');
    }

    // ==================== Global Edit Note Modal Helper ====================
    window.openEditModal = function(buttonElement) {
        if (!buttonElement) return;
        const id = buttonElement.dataset.id;
        const title = buttonElement.dataset.title || '';
        const content = buttonElement.dataset.content || '';
        const subject = buttonElement.dataset.subject || '';
        const tags = buttonElement.dataset.tags || '';
        const url = buttonElement.dataset.url || '';

        // Populate form fields
        const form = document.getElementById('globalEditForm');
        if (!form) return;
        form.action = url;
        document.getElementById('global_edit_title').value = title;
        document.getElementById('global_edit_content').value = content;
        document.getElementById('global_edit_subject').value = subject;
        document.getElementById('global_edit_tags').value = tags;

        openModal('globalEditNoteModal');
    };

    // ==================== ALL NOTES MODAL - SEARCH & FILTER ====================
    const allNotesSearch = document.getElementById('allNotesSearch');
    const noteSubjectFilter = document.getElementById('noteSubjectFilter');
    const noteSortFilter = document.getElementById('noteSortFilter');
    const allNotesCount = document.getElementById('all-notes-count');

    if (allNotesSearch) {
        allNotesSearch.addEventListener('input', filterAndSearchNotes);
    }
    if (noteSubjectFilter) {
        noteSubjectFilter.addEventListener('change', filterAndSearchNotes);
    }
    if (noteSortFilter) {
        noteSortFilter.addEventListener('change', filterAndSearchNotes);
    }

    function filterAndSearchNotes() {
        const searchTerm = (allNotesSearch?.value || '').toLowerCase();
        const selectedSubject = noteSubjectFilter?.value || 'all';
        const sortOrder = noteSortFilter?.value || 'newest';
        
        const noteCards = Array.from(document.querySelectorAll('#allNotesModal .note-card'));
        let visibleCount = 0;

        // Filter and search
        noteCards.forEach(card => {
            const title = card.dataset.title || '';
            const content = card.dataset.content || '';
            const tags = card.dataset.tags || '';
            const subject = card.dataset.subject || '';

            const matchesSearch = title.includes(searchTerm) || 
                                 content.includes(searchTerm) || 
                                 tags.includes(searchTerm);
            
            const matchesSubject = selectedSubject === 'all' || subject === selectedSubject;

            if (matchesSearch && matchesSubject) {
                card.style.display = 'block';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });

        // Sort visible cards
        const visibleCards = noteCards.filter(card => card.style.display !== 'none');
        sortNoteCards(visibleCards, sortOrder);

        // Update count
        if (allNotesCount) {
            allNotesCount.textContent = `(${visibleCount})`;
        }
    }

    function sortNoteCards(cards, sortOrder) {
        const container = document.querySelector('#allNotesModal .notes-grid');
        if (!container) return;

        cards.sort((a, b) => {
            const dateA = new Date(a.dataset.date);
            const dateB = new Date(b.dataset.date);
            const titleA = a.dataset.title;
            const titleB = b.dataset.title;

            switch(sortOrder) {
                case 'newest':
                    return dateB - dateA;
                case 'oldest':
                    return dateA - dateB;
                case 'title_asc':
                    return titleA.localeCompare(titleB);
                case 'title_desc':
                    return titleB.localeCompare(titleA);
                default:
                    return 0;
            }
        });

        cards.forEach(card => container.appendChild(card));
    }

    // ==================== COMPLETED TASKS MODAL - SEARCH & FILTER ====================
    const completedSearch = document.getElementById('completedTasksSearch');
    const completedPriorityFilter = document.getElementById('completedPriorityFilter');
    const completedSortFilter = document.getElementById('completedSortFilter');

    if (completedSearch) {
        completedSearch.addEventListener('input', filterCompletedTasks);
    }
    if (completedPriorityFilter) {
        completedPriorityFilter.addEventListener('change', filterCompletedTasks);
    }
    if (completedSortFilter) {
        completedSortFilter.addEventListener('change', filterCompletedTasks);
    }

    function filterCompletedTasks() {
        const searchTerm = (completedSearch?.value || '').toLowerCase();
        const selectedPriority = completedPriorityFilter?.value || 'all';
        const sortOrder = completedSortFilter?.value || 'newest';
        
        const taskItems = Array.from(document.querySelectorAll('#completedTasksModal .completed-task-item'));
        let visibleCount = 0;

        // Filter and search
        taskItems.forEach(item => {
            const title = item.dataset.title || '';
            const description = item.dataset.description || '';
            const priority = item.dataset.priority || '';

            const matchesSearch = title.includes(searchTerm) || description.includes(searchTerm);
            const matchesPriority = selectedPriority === 'all' || priority === selectedPriority;

            if (matchesSearch && matchesPriority) {
                item.style.display = 'flex';
                visibleCount++;
            } else {
                item.style.display = 'none';
            }
        });

        // Sort visible items
        const visibleItems = taskItems.filter(item => item.style.display !== 'none');
        sortTaskItems(visibleItems, sortOrder, 'completedTasksModal');

        // Update count
        updateModalCount('completedTasksModal', visibleCount);
    }

    // ==================== PENDING TASKS MODAL - SEARCH & FILTER ====================
    const pendingSearch = document.getElementById('pendingTasksSearch');
    const pendingPriorityFilter = document.getElementById('pendingPriorityFilter');
    const pendingSortFilter = document.getElementById('pendingSortFilter');

    if (pendingSearch) {
        pendingSearch.addEventListener('input', filterPendingTasks);
    }
    if (pendingPriorityFilter) {
        pendingPriorityFilter.addEventListener('change', filterPendingTasks);
    }
    if (pendingSortFilter) {
        pendingSortFilter.addEventListener('change', filterPendingTasks);
    }

    function filterPendingTasks() {
        const searchTerm = (pendingSearch?.value || '').toLowerCase();
        const selectedPriority = pendingPriorityFilter?.value || 'all';
        const sortOrder = pendingSortFilter?.value || 'due_date';
        
        const taskItems = Array.from(document.querySelectorAll('#pendingTasksModal .completed-task-item'));
        let visibleCount = 0;

        // Filter and search
        taskItems.forEach(item => {
            const title = item.dataset.title || '';
            const description = item.dataset.description || '';
            const priority = item.dataset.priority || '';

            const matchesSearch = title.includes(searchTerm) || description.includes(searchTerm);
            const matchesPriority = selectedPriority === 'all' || priority === selectedPriority;

            if (matchesSearch && matchesPriority) {
                item.style.display = 'flex';
                visibleCount++;
            } else {
                item.style.display = 'none';
            }
        });

        // Sort visible items
        const visibleItems = taskItems.filter(item => item.style.display !== 'none');
        sortTaskItems(visibleItems, sortOrder, 'pendingTasksModal');

        // Update count
        updateModalCount('pendingTasksModal', visibleCount);
    }

    // ==================== OVERDUE TASKS MODAL - SEARCH & FILTER ====================
    const overdueSearch = document.getElementById('overdueTasksSearch');
    const overduePriorityFilter = document.getElementById('overduePriorityFilter');
    const overdueSortFilter = document.getElementById('overdueSortFilter');

    if (overdueSearch) {
        overdueSearch.addEventListener('input', filterOverdueTasks);
    }
    if (overduePriorityFilter) {
        overduePriorityFilter.addEventListener('change', filterOverdueTasks);
    }
    if (overdueSortFilter) {
        overdueSortFilter.addEventListener('change', filterOverdueTasks);
    }

    function filterOverdueTasks() {
        const searchTerm = (overdueSearch?.value || '').toLowerCase();
        const selectedPriority = overduePriorityFilter?.value || 'all';
        const sortOrder = overdueSortFilter?.value || 'most_overdue';
        
        const taskItems = Array.from(document.querySelectorAll('#overdueTasksModal .completed-task-item'));
        let visibleCount = 0;

        // Filter and search
        taskItems.forEach(item => {
            const title = item.dataset.title || '';
            const description = item.dataset.description || '';
            const priority = item.dataset.priority || '';

            const matchesSearch = title.includes(searchTerm) || description.includes(searchTerm);
            const matchesPriority = selectedPriority === 'all' || priority === selectedPriority;

            if (matchesSearch && matchesPriority) {
                item.style.display = 'flex';
                visibleCount++;
            } else {
                item.style.display = 'none';
            }
        });

        // Sort visible items
        const visibleItems = taskItems.filter(item => item.style.display !== 'none');
        sortTaskItems(visibleItems, sortOrder, 'overdueTasksModal');

        // Update count
        updateModalCount('overdueTasksModal', visibleCount);
    }

    // ==================== UTILITY FUNCTIONS ====================
    function sortTaskItems(items, sortOrder, modalId) {
        const container = document.querySelector(`#${modalId} .completed-tasks-list`);
        if (!container) return;

        items.sort((a, b) => {
            const dateA = new Date(a.dataset.date);
            const dateB = new Date(b.dataset.date);
            const titleA = a.dataset.title;
            const titleB = b.dataset.title;
            const priorityOrder = { high: 3, medium: 2, low: 1 };
            const priorityA = priorityOrder[a.dataset.priority] || 0;
            const priorityB = priorityOrder[b.dataset.priority] || 0;

            switch(sortOrder) {
                case 'newest':
                    return dateB - dateA;
                case 'oldest':
                    return dateA - dateB;
                case 'due_date':
                    return dateA - dateB;
                case 'most_overdue':
                    return dateA - dateB;
                case 'priority_high':
                    return priorityB - priorityA;
                case 'priority_low':
                    return priorityA - priorityB;
                case 'title_asc':
                    return titleA.localeCompare(titleB);
                case 'title_desc':
                    return titleB.localeCompare(titleA);
                default:
                    return 0;
            }
        });

        items.forEach(item => container.appendChild(item));
    }

    function updateModalCount(modalId, count) {
        const countElement = document.querySelector(`#${modalId} .modal-count`);
        if (countElement) {
            countElement.textContent = `(${count})`;
        }
    }

    // ==================== AJAX Add Note Submission ====================
    const addNoteForm = document.getElementById('addNoteForm');
    if (addNoteForm) {
        addNoteForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const formData = new FormData(addNoteForm);
            const fetchOptions = {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: formData
            };

            fetch(addNoteForm.action, fetchOptions)
                .then(resp => {
                    if (!resp.ok) throw resp;
                    return resp.json();
                })
                .then(data => {
                    if (data.status === 'ok') {
                        // close modal
                        closeModal('addNoteModal');

                        // insert into compact notes list (top)
                        try {
                            const notesSection = document.querySelector('.card.notes');
                            if (notesSection) {
                                const container = notesSection.querySelector('.card-header').nextElementSibling;
                                // create new compact note element
                                const noteElem = createCompactNoteElement(data.note);
                                if (container) {
                                    container.parentNode.insertBefore(noteElem, container);
                                } else {
                                    // fallback: append to notes section
                                    notesSection.insertBefore(noteElem, notesSection.querySelector('.card-header').nextSibling);
                                }
                            }
                        } catch (err) {
                            console.warn('Could not insert compact note element', err);
                        }

                        // insert into All Notes grid
                        const allNotesGrid = document.querySelector('#allNotesModal .notes-grid');
                        if (allNotesGrid) {
                            const card = document.createElement('div');
                            card.className = 'note-card';
                            card.setAttribute('data-title', (data.note.title || '').toLowerCase());
                            card.setAttribute('data-content', (data.note.content || '').toLowerCase());
                            card.setAttribute('data-tags', (data.note.tags || '').toLowerCase());
                            card.innerHTML = `
                                <div class="note-card-header" style="position:relative;">
                                  <h4>${escapeHtml(data.note.title)}</h4>
                                  <span class="note-date">${escapeHtml(data.note.created_at)}</span>
                                </div>
                                <div class="note-card-body">
                                  <p>${escapeHtml(truncateWords(data.note.content, 30))}</p>
                                </div>
                                <div class="note-card-footer">
                                  ${data.note.subject ? `<span class="note-subject">${escapeHtml(data.note.subject)}</span>` : ''}
                                </div>
                            `;
                            allNotesGrid.prepend(card);
                        }

                        // update counts
                        const totalNode = document.querySelector('.stat-card .stat-number');
                        const totalNotesEls = document.querySelectorAll('#all-notes-count, #sidebar-notes-count');
                        if (data.total_notes) {
                            totalNotesEls.forEach(el => el.textContent = `(${data.total_notes})`);
                            // update overview card number (Total Notes stat-card)
                            const statCards = document.querySelectorAll('.stat-card');
                            statCards.forEach(card => {
                                const h4 = card.querySelector('h4');
                                if (h4 && h4.textContent.trim() === 'Total Notes') {
                                    const statNum = card.querySelector('.stat-number');
                                    if (statNum) statNum.textContent = data.total_notes;
                                }
                            });
                        }

                        showNotification('Note created', 'success');

                        // reset form
                        addNoteForm.reset();
                    }
                })
                .catch(err => {
                    console.error('Add note failed', err);
                    showNotification('Failed to create note', 'error');
                });
        });
    }

    // Helper: create compact note DOM element (small card used in main dashboard list)
    function createCompactNoteElement(note) {
        const wrapper = document.createElement('div');
        wrapper.className = 'note';
        wrapper.innerHTML = `
            <div style="position:relative;">
              <h4>${escapeHtml(note.title)}</h4>
            </div>
            <p>${escapeHtml(truncateWords(note.content, 15))}</p>
            <span class="date">${escapeHtml(note.created_at)}</span>
            <div class="note-actions" style="margin-top:8px;">
              <button type="button" class="btn btn-sm" style="margin-right:6px;"
                      onclick="openEditModal(this)"
                      data-id="${note.id}"
                      data-title="${escapeHtml(note.title)}"
                      data-content="${escapeHtml(note.content)}"
                      data-subject="${escapeHtml(note.subject)}"
                      data-tags="${escapeHtml(note.tags)}"
                      data-url="${note.edit_url}">✏️ Edit</button>
              <form method="post" action="${note.delete_url}" style="display:inline;">
                <input type="hidden" name="csrfmiddlewaretoken" value="">
                <button type="submit" class="btn btn-sm btn-danger" onclick="return confirm('Delete this note?');">🗑️ Delete</button>
              </form>
            </div>
        `;
        return wrapper;
    }

    function truncateWords(text, num) {
        if (!text) return '';
        const words = text.split(/\s+/);
        if (words.length <= num) return text;
        return words.slice(0, num).join(' ') + '...';
    }

    function escapeHtml(unsafe) {
        if (unsafe === null || unsafe === undefined) return '';
        return String(unsafe)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    function openModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }
    }

    function closeModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
            
            // Reset filters when closing
            if (modalId === 'completedTasksModal' && completedSearch) {
                completedSearch.value = '';
                if (completedPriorityFilter) completedPriorityFilter.value = 'all';
                if (completedSortFilter) completedSortFilter.value = 'newest';
                filterCompletedTasks();
            } else if (modalId === 'pendingTasksModal' && pendingSearch) {
                pendingSearch.value = '';
                if (pendingPriorityFilter) pendingPriorityFilter.value = 'all';
                if (pendingSortFilter) pendingSortFilter.value = 'due_date';
                filterPendingTasks();
            } else if (modalId === 'overdueTasksModal' && overdueSearch) {
                overdueSearch.value = '';
                if (overduePriorityFilter) overduePriorityFilter.value = 'all';
                if (overdueSortFilter) overdueSortFilter.value = 'most_overdue';
                filterOverdueTasks();
            } else if (modalId === 'allNotesModal' && allNotesSearch) {
                allNotesSearch.value = '';
                if (noteSubjectFilter) noteSubjectFilter.value = 'all';
                if (noteSortFilter) noteSortFilter.value = 'newest';
                filterAndSearchNotes();
            }
        }
    }

    // Close modal when clicking outside
    window.onclick = function(event) {
        if (event.target.classList.contains('modal')) {
            const modalId = event.target.id;
            closeModal(modalId);
        }
    }

    // Close modal with ESC key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal');
            modals.forEach(modal => {
                if (modal.style.display === 'flex' || modal.style.display === 'block') {
                    closeModal(modal.id);
                }
            });
        }
    });

    // Make functions globally accessible
    window.openCompletedTasksModal = openCompletedTasksModal;
    window.openPendingTasksModal = openPendingTasksModal;
    window.openOverdueTasksModal = openOverdueTasksModal;
    window.openAllNotesModal = openAllNotesModal;
    window.closeModal = closeModal;

    // ==================== Welcome Message ====================
    const userNameElement = document.querySelector('.topbar-left h2');
    if (userNameElement) {
        const userName = userNameElement.textContent.replace('Welcome, ', '').replace('Good morning, ', '').replace('Good afternoon, ', '').replace('Good evening, ', '');
        const hour = new Date().getHours();
        let greeting = '';
        
        if (hour < 12) greeting = 'Good morning';
        else if (hour < 18) greeting = 'Good afternoon';
        else greeting = 'Good evening';
        
        userNameElement.textContent = `${greeting}, ${userName}!`;
    }

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

    // =======================
    // 🔔 Notification Modal Logic
    // =======================
    const bell = document.getElementById("notificationBell");
    const notifModal = document.getElementById("notificationModal");
    const closeNotificationModal = document.getElementById("closeNotificationModal");

    if (bell && notifModal && closeNotificationModal) {
        // Open modal when bell is clicked
        bell.addEventListener("click", () => {
            notifModal.style.display = "flex";
        });

        // Close modal when X is clicked
        closeNotificationModal.addEventListener("click", () => {
            notifModal.style.display = "none";
        });

        // Close modal when clicking outside the content
        window.addEventListener("click", (event) => {
            if (event.target === notifModal) {
                notifModal.style.display = "none";
            }
        });
    } else {
        console.warn("Notification modal elements not found in DOM.");
    }

    console.log('✅ StuNotes Dashboard Enhanced!');
    console.log('💡 Keyboard shortcuts:');
    console.log('   - Ctrl/Cmd + N: Add new task');
    console.log('   - ESC: Close task form');
    console.log('🎯 All search and filter features loaded!');

});