// Configuration
const API_BASE_URL = "http://127.0.0.1:8000"; 
let currentVideoUrl = null;

// --- DOM ELEMENTS ---
// Pages
const landingPage = document.getElementById('landing-page');
const appPage = document.getElementById('app-page');

// Auth Containers
const loginContainer = document.getElementById('login-container');
const signupContainer = document.getElementById('signup-container');

// Auth Forms & Inputs
const loginForm = document.getElementById('login-form');
const signupForm = document.getElementById('signup-form');
const loginUsernameInput = document.getElementById('login-username');
const loginPasswordInput = document.getElementById('login-password');
const signupUsernameInput = document.getElementById('signup-username');
const signupEmailInput = document.getElementById('signup-email');
const signupPasswordInput = document.getElementById('signup-password');

// Auth Toggles
const showSignupBtn = document.getElementById('show-signup');
const showLoginBtn = document.getElementById('show-login');

// App Interface
const loadVideoBtn = document.getElementById('load-video-btn');
const youtubeUrlInput = document.getElementById('youtube-url');
const videoContextDiv = document.getElementById('video-context');
const videoThumb = document.getElementById('video-thumb');
const videoTitle = document.getElementById('video-title');
const channelName = document.getElementById('channel-name');
const chatWindow = document.getElementById('chat-window');
const userQueryInput = document.getElementById('user-query');
const sendBtn = document.getElementById('send-btn');
const historyList = document.getElementById('history-list');

// New Buttons
const newChatBtn = document.getElementById('new-chat-btn');
const signOutBtn = document.getElementById('sign-out-btn');


// --- INITIALIZATION ---
// Check if user is already logged in when page loads
window.addEventListener('load', () => {
    const token = localStorage.getItem('accessToken');
    if (token) {
        landingPage.classList.add('hidden');
        appPage.classList.remove('hidden');
        renderHistory(); // Load history from LocalStorage
    }
});


// --- AUTH UI HANDLERS ---

// Toggle to Signup
showSignupBtn.addEventListener('click', () => {
    loginContainer.classList.add('hidden');
    signupContainer.classList.remove('hidden');
});

// Toggle to Login
showLoginBtn.addEventListener('click', () => {
    signupContainer.classList.add('hidden');
    loginContainer.classList.remove('hidden');
});

// Sign Out Logic
if (signOutBtn) {
    signOutBtn.addEventListener('click', () => {
        if(confirm("Are you sure you want to sign out?")) {
            localStorage.removeItem('accessToken');
            location.reload(); // Reload page to return to login screen
        }
    });
}


// --- AUTH LOGIC ---

// 1. HANDLE SIGNUP
signupForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = signupUsernameInput.value;
    const email = signupEmailInput.value;
    const password = signupPasswordInput.value;
    const errorDiv = document.getElementById('signup-error');
    const btn = signupForm.querySelector('button');

    // UI Reset
    errorDiv.style.display = 'none';
    btn.textContent = "Creating Account...";
    btn.disabled = true;

    try {
        const response = await fetch(`${API_BASE_URL}/auth/signup`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Signup failed');
        }

        alert("Account created! Please log in.");
        signupForm.reset();
        signupContainer.classList.add('hidden');
        loginContainer.classList.remove('hidden');

    } catch (error) {
        errorDiv.textContent = error.message;
        errorDiv.style.display = 'block';
    } finally {
        btn.textContent = "Sign Up";
        btn.disabled = false;
    }
});

// 2. HANDLE LOGIN
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = loginUsernameInput.value;
    const password = loginPasswordInput.value;
    const errorDiv = document.getElementById('login-error');
    const btn = loginForm.querySelector('button');

    // UI Reset
    errorDiv.style.display = 'none';
    btn.textContent = "Signing In...";
    btn.disabled = true;

    try {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        const response = await fetch(`${API_BASE_URL}/auth/token`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Incorrect username or password');
        }

        // Success: Store Token
        localStorage.setItem('accessToken', data.access_token);
        
        // Switch to App Page & Render History
        landingPage.classList.add('hidden');
        appPage.classList.remove('hidden');
        renderHistory();

    } catch (error) {
        errorDiv.textContent = error.message;
        errorDiv.style.display = 'block';
    } finally {
        btn.textContent = "Sign In";
        btn.disabled = false;
    }
});


// --- APP LOGIC ---

// New Chat Button Handler
if (newChatBtn) {
    newChatBtn.addEventListener('click', () => {
        // Reset App State
        currentVideoUrl = null;
        videoContextDiv.classList.add('hidden');
        youtubeUrlInput.value = "";
        
        // Clear Chat Window
        chatWindow.innerHTML = `
            <div class="message bot-message">
                New session started. Load a video to begin!
            </div>
        `;
    });
}

// VIDEO INFO HANDLER
loadVideoBtn.addEventListener('click', async () => {
    const url = youtubeUrlInput.value.trim();
    if (!url) return alert("Please enter a URL");

    await fetchVideoData(url);
});

async function fetchVideoData(url) {
    loadVideoBtn.textContent = "Loading...";
    try {
        const response = await fetch(`${API_BASE_URL}/video_info?video_url=${encodeURIComponent(url)}`);
        const data = await response.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        // Update UI
        currentVideoUrl = url;
        videoThumb.src = data.thumbnail;
        videoTitle.textContent = data.title;
        channelName.textContent = data.channel;
        
        videoContextDiv.classList.remove('hidden');
        addSystemMessage(`Video loaded: "${data.title}". What would you like to know?`);
        
        // Save to History (LocalStorage)
        saveToHistory({
            title: data.title,
            url: url,
            thumbnail: data.thumbnail
        });

    } catch (error) {
        console.error("Error fetching video info:", error);
        alert("Failed to fetch video info. Is the backend running?");
    } finally {
        loadVideoBtn.textContent = "Load Video";
    }
}

// CHAT HANDLER
async function handleChat() {
    const query = userQueryInput.value.trim();
    if (!query) return;
    if (!currentVideoUrl) return alert("Please load a video first!");

    addUserMessage(query);
    userQueryInput.value = "";
    userQueryInput.focus();

    const loadingId = addLoadingMessage();

    try {
        const response = await fetch(`${API_BASE_URL}/ask/?url=${encodeURIComponent(currentVideoUrl)}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query })
        });

        const data = await response.json();
        removeMessage(loadingId);
        
        let answerText = data;
        if (typeof data === 'object' && data !== null) {
            answerText = data.answer || data.response || data.result || data.content || JSON.stringify(data);
        }
        
        addBotMessage(answerText);

    } catch (error) {
        removeMessage(loadingId);
        addSystemMessage("Error: Could not get response from backend.");
        console.error(error);
    }
}

// Event Listeners for Chat
sendBtn.addEventListener('click', handleChat);
userQueryInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleChat();
});


// --- HISTORY MANAGEMENT (LOCALSTORAGE) ---

function getHistory() {
    const history = localStorage.getItem('talkToTube_history');
    return history ? JSON.parse(history) : [];
}

function saveToHistory(newItem) {
    let history = getHistory();
    
    // Prevent duplicates
    const exists = history.some(item => item.url === newItem.url);
    if (!exists) {
        history.unshift(newItem); // Add to top
        if(history.length > 10) history.pop(); // Limit to 10
        
        localStorage.setItem('talkToTube_history', JSON.stringify(history));
        renderHistory();
    }
}

function deleteHistoryItem(index) {
    let history = getHistory();
    history.splice(index, 1);
    localStorage.setItem('talkToTube_history', JSON.stringify(history));
    renderHistory();
}

function renderHistory() {
    historyList.innerHTML = '';
    const history = getHistory();

    if (history.length === 0) {
        historyList.innerHTML = '<div style="padding:10px; color:#aaa; font-size:0.8rem; text-align:center">No history yet</div>';
        return;
    }

    history.forEach((item, index) => {
        const div = document.createElement('div');
        div.className = 'history-item';
        
        div.innerHTML = `
            <span class="history-text" title="${item.title}">${item.title}</span>
            <button class="delete-history-btn" title="Delete">×</button>
        `;

        // Load video on click
        div.querySelector('.history-text').addEventListener('click', () => {
            youtubeUrlInput.value = item.url;
            fetchVideoData(item.url);
        });

        // Delete on click
        div.querySelector('.delete-history-btn').addEventListener('click', (e) => {
            e.stopPropagation();
            deleteHistoryItem(index);
        });

        historyList.appendChild(div);
    });
}


// --- UI HELPERS ---

function addUserMessage(text) {
    const div = document.createElement('div');
    div.className = 'message user-message';
    div.textContent = text;
    chatWindow.appendChild(div);
    scrollToBottom();
}

function addBotMessage(text) {
    const div = document.createElement('div');
    div.className = 'message bot-message';
    div.textContent = text;
    chatWindow.appendChild(div);
    scrollToBottom();
}

function addSystemMessage(text) {
    const div = document.createElement('div');
    div.className = 'message bot-message';
    div.style.fontStyle = 'italic';
    div.textContent = text;
    chatWindow.appendChild(div);
    scrollToBottom();
}

function addLoadingMessage() {
    const id = 'loading-' + Date.now();
    const div = document.createElement('div');
    div.id = id;
    div.className = 'message bot-message loading-dots';
    div.textContent = "Thinking...";
    chatWindow.appendChild(div);
    scrollToBottom();
    return id;
}

function removeMessage(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

function scrollToBottom() {
    chatWindow.scrollTop = chatWindow.scrollHeight;
}