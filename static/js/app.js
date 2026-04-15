import API from './api.js';

document.addEventListener('DOMContentLoaded', () => {
    // UI Elements
    const threadList = document.getElementById('thread-list');
    const storyboardContainer = document.getElementById('storyboard-container');
    const narrativeInput = document.getElementById('narrative-input');
    const generateBtn = document.getElementById('generate-btn');
    const loader = document.getElementById('loader');
    const styleSelect = document.getElementById('style-select');
    const selectedStyleLabel = document.getElementById('selected-style');
    const dropdownOptions = document.getElementById('dropdown-options');

    let currentThreadId = null;

    // --- Authentication Check ---
    const token = localStorage.getItem('access_token');
    const user = JSON.parse(localStorage.getItem('user') || 'null');
    if (!token || !user) {
        window.location.href = '/login';
        return;
    }

    // --- Thread Management ---

    const renderThreads = async () => {
        try {
            const threads = await API.listThreads();
            if (!threadList) return;
            threadList.innerHTML = '';

            const groups = { 'Today': [], 'Yesterday': [], 'Previous': [] };
            const now = new Date();
            const yesterday = new Date();
            yesterday.setDate(now.getDate() - 1);

            [...threads].reverse().forEach(thread => {
                const threadDate = new Date(thread.created_at);
                if (threadDate.toDateString() === now.toDateString()) {
                    groups['Today'].push(thread);
                } else if (threadDate.toDateString() === yesterday.toDateString()) {
                    groups['Yesterday'].push(thread);
                } else {
                    groups['Previous'].push(thread);
                }
            });

            Object.keys(groups).forEach(groupName => {
                if (groups[groupName].length === 0) return;

                const header = document.createElement('div');
                header.className = 'thread-group-header';
                header.innerText = groupName;
                threadList.appendChild(header);

                groups[groupName].forEach(thread => {
                    const item = document.createElement('div');
                    item.className = `thread-item ${currentThreadId === thread.thread_id ? 'active' : ''}`;
                    item.innerHTML = `
                        <div class="thread-main">
                            <div class="thread-info" title="${thread.title}">${thread.title}</div>
                        </div>
                        <div class="delete-thread" data-id="${thread.thread_id}">
                            <span class="delete-icon">×</span>
                        </div>
                    `;

                    item.onclick = (e) => {
                        if (e.target.closest('.delete-thread')) return;
                        switchThread(thread.thread_id);
                    };

                    const delBtn = item.querySelector('.delete-thread');
                    delBtn.onclick = async (e) => {
                        e.stopPropagation();
                        if (confirm('Delete this storyboard?')) {
                            await API.deleteThread(thread.thread_id);
                            if (currentThreadId === thread.thread_id) {
                                startNewChat();
                            } else {
                                renderThreads();
                            }
                        }
                    };
                    threadList.appendChild(item);
                });
            });
        } catch (err) {
            console.error('Failed to load threads:', err);
        }
    };

    const switchThread = async (threadId) => {
        try {
            currentThreadId = threadId;
            if (storyboardContainer) storyboardContainer.innerHTML = '';
            if (loader) loader.style.display = 'block';

            const thread = await API.getThread(threadId);

            if (thread && thread.messages) {
                const lastBotMsg = [...thread.messages].reverse().find(m => m.bot && m.bot.storyboard);
                if (lastBotMsg && lastBotMsg.bot.storyboard) {
                    renderStoryboard(lastBotMsg.bot.storyboard);
                }
            }
            renderThreads();
        } catch (error) {
            console.error("Error switching thread:", error);
        } finally {
            if (loader) loader.style.display = 'none';
        }
    };

    const startNewChat = () => {
        currentThreadId = null;
        if (storyboardContainer) storyboardContainer.innerHTML = '';
        if (narrativeInput) narrativeInput.value = '';
        renderThreads();
    };

    const renderStoryboard = (panels) => {
        if (!storyboardContainer) return;
        storyboardContainer.innerHTML = panels.map((p, i) => `
            <div class="panel">
                <img src="${p.image_url}" alt="Panel ${i+1}" loading="lazy">
                <div class="panel-content">
                    <div class="panel-text">${p.text}</div>
                    <div class="panel-prompt">${p.prompt}</div>
                </div>
            </div>
        `).join('');
        storyboardContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    };

    // --- Generation Logic ---

    if (generateBtn) {
        generateBtn.onclick = async () => {
            const text = narrativeInput.value.trim();
            if(!text) return alert("Please enter a narrative.");

            if(!currentThreadId) {
                try {
                    const newThread = await API.createThread();
                    currentThreadId = newThread.thread_id;
                } catch (e) {
                    return alert("Failed to create storyboard session: " + e.message);
                }
            }

            if (storyboardContainer) storyboardContainer.innerHTML = '';
            if (loader) loader.style.display = 'block';
            generateBtn.disabled = true;

            try {
                const style = styleSelect ? styleSelect.value : 'digital_art';
                const data = await API.sendMessage(text, currentThreadId, style);
                
                if(data.storyboard) {
                    renderStoryboard(data.storyboard);
                    renderThreads(); 
                } else {
                    alert("Error: " + (data.message || "Generation failed"));
                }
            } catch (e) {
                alert("Error: " + e.message);
            } finally {
                if (loader) loader.style.display = 'none';
                generateBtn.disabled = false;
            }
        };
    }

    // --- Dropdown Management ---

    window.toggleDropdown = () => {
        if (dropdownOptions) dropdownOptions.classList.toggle('active');
    };

    window.selectStyle = (val, label) => {
        if (styleSelect) styleSelect.value = val;
        if (selectedStyleLabel) selectedStyleLabel.innerText = label;
        if (dropdownOptions) dropdownOptions.classList.remove('active');
    };

    window.addEventListener('click', (e) => {
        const styleDropdown = document.getElementById('style-dropdown');
        if (styleDropdown && !styleDropdown.contains(e.target)) {
            if (dropdownOptions) dropdownOptions.classList.remove('active');
        }
    });

    // --- Global Actions ---

    window.logout = () => {
        localStorage.clear();
        window.location.href = '/login';
    };

    window.startNewChat = startNewChat;
    window.selectThread = switchThread;

    // --- Initialize ---
    renderThreads();
});
