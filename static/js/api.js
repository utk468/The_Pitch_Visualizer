const API_BASE = '/api';

const API = {
    // Auth Methods
    login: async (email, password) => {
        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Login failed');
        }
        return await response.json();
    },

    register: async (name, email, password) => {
        const response = await fetch(`${API_BASE}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, password })
        });
        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Registration failed');
        }
        return await response.json();
    },

    // Thread Methods
    createThread: async () => {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${API_BASE}/threads/?token=${token}`, {
            method: 'POST'
        });
        if (!response.ok) {
            const err = await response.json();
            const detail = typeof err.detail === 'string' ? err.detail : JSON.stringify(err.detail);
            throw new Error(detail || 'Failed to create thread');
        }
        return await response.json();
    },

    listThreads: async () => {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${API_BASE}/threads/?token=${token}`);
        if (!response.ok) {
            const err = await response.json();
            const detail = typeof err.detail === 'string' ? err.detail : JSON.stringify(err.detail);
            throw new Error(detail || 'Failed to list threads');
        }
        return await response.json();
    },

    deleteThread: async (threadId) => {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${API_BASE}/threads/${threadId}?token=${token}`, {
            method: 'DELETE'
        });
        if (!response.ok) {
            const err = await response.json();
            const detail = typeof err.detail === 'string' ? err.detail : JSON.stringify(err.detail);
            throw new Error(detail || 'Failed to delete thread');
        }
        return await response.json();
    },

    getThread: async (threadId) => {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${API_BASE}/threads/${threadId}?token=${token}`);
        if (!response.ok) {
            const err = await response.json();
            const detail = typeof err.detail === 'string' ? err.detail : JSON.stringify(err.detail);
            throw new Error(detail || 'Failed to get thread');
        }
        return await response.json();
    },

    // Chat Methods
    sendMessage: async (message, threadId, history = []) => {
        const token = localStorage.getItem('access_token');
        const user = JSON.parse(localStorage.getItem('user') || '{}');

        const response = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ 
                message, 
                thread_id: threadId,
                history,
                user_name: user.name,
                user_email: user.email,
                user_id: user.id
            })
        });
        if (!response.ok) {
            const err = await response.json();
            const detail = typeof err.detail === 'string' ? err.detail : JSON.stringify(err.detail);
            throw new Error(detail || 'Chat failed');
        }
        return await response.json();
    }
};

export default API;
