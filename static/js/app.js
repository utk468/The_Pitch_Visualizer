import API from './api.js';

document.addEventListener('DOMContentLoaded', () => {
    // Chat Elements
    const chatHistory = document.getElementById('chat-history');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const riskBadge = document.getElementById('risk-badge');
    const symptomList = document.getElementById('symptom-list');
    
    // Thread Elements
    const threadList = document.getElementById('thread-list');
    const newChatBtn = document.getElementById('new-chat-btn');
    const logoutBtn = document.getElementById('logout-btn');

    let history = [];
    let currentThreadId = null;

    // --- Authentication ---
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/login';
        return;
    }

    // Logout Logic
    logoutBtn.onclick = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
    };

    // --- Thread Management ---

    const renderThreads = async () => {
        const threads = await API.listThreads();
        threadList.innerHTML = '';
        
        // Grouping logic
        const groups = {
            'Today': [],
            'Yesterday': [],
            'Previous': []
        };

        const now = new Date();
        const yesterday = new Date();
        yesterday.setDate(now.getDate() - 1);

        threads.reverse().forEach(thread => {
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
                        <i data-lucide="message-square" style="width: 14px; height: 14px; opacity: 0.6;"></i>
                        <div class="thread-info" title="${thread.title}">${thread.title}</div>
                    </div>
                    <div class="delete-thread" data-id="${thread.thread_id}">
                        <i data-lucide="x" style="width: 14px; height: 14px;"></i>
                    </div>
                `;
                
                item.onclick = (e) => {
                    if (e.target.closest('.delete-thread')) return;
                    switchThread(thread.thread_id);
                };

                const delBtn = item.querySelector('.delete-thread');
                delBtn.onclick = async (e) => {
                    e.stopPropagation();
                    if (confirm('Delete this conversation?')) {
                        await API.deleteThread(thread.thread_id);
                        if (currentThreadId === thread.thread_id) {
                            currentThreadId = null;
                            chatHistory.innerHTML = '';
                        }
                        renderThreads();
                    }
                };
                threadList.appendChild(item);
            });
        });
        
        lucide.createIcons();
    };

    const switchThread = async (threadId) => {
        try {
            console.log(`Switching to thread: ${threadId}`);
            currentThreadId = threadId;
            const thread = await API.getThread(threadId);
            
            // Clear UI
            chatHistory.innerHTML = '';
            history = [];
            
            if (thread && thread.messages) {
                console.log(`Loading ${thread.messages.length} messages`);
                // Load messages
                thread.messages.forEach(msg => {
                    // 1. Check for new nested structure
                    let text = "";
                    let role = "";

                    if (msg.user) {
                        text = msg.user.query;
                        role = "user";
                    } else if (msg.bot) {
                        text = msg.bot.response;
                        role = "bot";
                    } else {
                        // 2. Fallback for older flat/split structures
                        text = msg.query || msg.response || msg.content || "";
                        role = msg.role || (msg.query ? "user" : "bot");
                    }

                    if (text) {
                        appendMessage(text, role);
                        history.push(text);
                    }
                });

                // Update Dashboard with last bot message
                const lastMsgWithBot = [...thread.messages].reverse().find(m => m.bot || (m.role === 'bot'));
                const lastBotData = lastMsgWithBot ? (lastMsgWithBot.bot || lastMsgWithBot) : null;
                
                if (lastBotData) {
                    updateDashboard(lastBotData.risk_level, lastBotData.symptoms);
                } else {
                    updateDashboard('Normal', []);
                }
            } else {
                console.warn("Thread has no messages or failed to load");
                updateDashboard('Normal', []);
            }

            renderThreads();
        } catch (error) {
            console.error("Error switching thread:", error);
            appendMessage("Failed to load conversation history.", "bot");
        }
    };

    newChatBtn.onclick = async () => {
        const newThread = await API.createThread();
        currentThreadId = newThread.thread_id;
        chatHistory.innerHTML = '';
        history = [];
        updateDashboard('Normal', []);
        renderThreads();
    };

    // Initialize
    renderThreads();

    // --- Chat Logic ---

    const appendMessage = (text, sender) => {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `message-${sender}`);
        messageDiv.innerText = text;
        chatHistory.appendChild(messageDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    };

    const updateDashboard = (risk, symptoms) => {
        riskBadge.innerText = risk || 'Normal';
        riskBadge.className = 'risk-badge';
        const lowerRisk = (risk || 'Normal').toLowerCase();
        if (lowerRisk.includes('emergency')) {
            riskBadge.classList.add('risk-emergency');
        } else if (lowerRisk.includes('moderate')) {
            riskBadge.classList.add('risk-moderate');
        } else {
            riskBadge.classList.add('risk-normal');
        }

        symptomList.innerHTML = '';
        if (!symptoms || symptoms.length === 0) {
            symptomList.innerHTML = '<span style="color: var(--text-muted); font-size: 0.8rem;">None detected</span>';
        } else {
            symptoms.forEach(s => {
                const tag = document.createElement('span');
                tag.classList.add('symptom-tag');
                tag.innerText = s;
                symptomList.appendChild(tag);
            });
        }
    };

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const msg = chatInput.value.trim();
        if (!msg) return;

        // If no thread, create one first
        if (!currentThreadId) {
            const newThread = await API.createThread();
            currentThreadId = newThread.thread_id;
        }

        appendMessage(msg, 'user');
        chatInput.value = '';
        
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('message', 'message-bot');
        typingDiv.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';
        chatHistory.appendChild(typingDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;

        try {
            const data = await API.sendMessage(msg, currentThreadId, history);
            chatHistory.removeChild(typingDiv);
            appendMessage(data.response, 'bot');
            updateDashboard(data.risk_level, data.symptoms);
            history.push(msg);
            history.push(data.response);
            
            // Re-render threads to update titles if first message
            if (history.length <= 2) {
                renderThreads();
            }
        } catch (err) {
            chatHistory.removeChild(typingDiv);
            appendMessage('Error: ' + err.message, 'bot');
            
            if (err.message.includes('Unauthorized')) {
                window.location.href = '/login';
            }
        }
    });
});
