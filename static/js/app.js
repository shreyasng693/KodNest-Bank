// Use relative URL for API (works both locally and on Vercel)
const API_BASE_URL = '';

// DOM Elements
const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');
const loginContainer = document.getElementById('loginContainer');
const registerContainer = document.getElementById('registerContainer');
const dashboardContainer = document.getElementById('dashboardContainer');
const messageBox = document.getElementById('messageBox');
const balanceDisplay = document.getElementById('balanceDisplay');
const userInfo = document.getElementById('userInfo');
const logoutBtn = document.getElementById('logoutBtn');
const checkBalanceBtn = document.getElementById('checkBalanceBtn');

// Helper function to get token
function getToken() {
    return localStorage.getItem('jwt_token');
}

// Helper function to set token
function setToken(token) {
    localStorage.setItem('jwt_token', token);
}

// Helper function to remove token
function removeToken() {
    localStorage.removeItem('jwt_token');
}

// Show message
function showMessage(message, type) {
    messageBox.textContent = message;
    messageBox.className = `message ${type}`;
    messageBox.style.display = 'block';
    setTimeout(() => {
        messageBox.style.display = 'none';
    }, 5000);
}

// Switch between login and register
function showRegister() {
    loginContainer.classList.add('hidden');
    registerContainer.classList.remove('hidden');
}

function showLogin() {
    registerContainer.classList.add('hidden');
    loginContainer.classList.remove('hidden');
}

// Show dashboard
function showDashboard(userData) {
    loginContainer.classList.add('hidden');
    registerContainer.classList.add('hidden');
    dashboardContainer.classList.remove('hidden');
    userInfo.textContent = `Welcome, ${userData.username}!`;
    balanceDisplay.textContent = '---';
}

// Check if user is logged in
async function checkAuth() {
    const token = getToken();
    if (!token) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/verify`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        const data = await response.json();
        
        if (data.valid) {
            showDashboard(data.data);
        } else {
            removeToken();
        }
    } catch (error) {
        console.log('Not authenticated');
        removeToken();
    }
}

// Register form submission
if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const submitBtn = registerForm.querySelector('.btn');
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="loading"></span>Registering...';
        
        const formData = {
            uid: document.getElementById('regUid').value,
            username: document.getElementById('regUsername').value,
            email: document.getElementById('regEmail').value,
            password: document.getElementById('regPassword').value,
            phone: document.getElementById('regPhone').value,
            role: 'Customer'
        };
        
        try {
            const response = await fetch(`${API_BASE_URL}/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                showMessage(data.message, 'success');
                setTimeout(() => {
                    showLogin();
                    registerForm.reset();
                }, 1500);
            } else {
                showMessage(data.message, 'error');
            }
        } catch (error) {
            showMessage('Registration failed. Please try again.', 'error');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Register';
        }
    });
}

// Login form submission
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const submitBtn = loginForm.querySelector('.btn');
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="loading"></span>Logging in...';
        
        const formData = {
            username: document.getElementById('loginUsername').value,
            password: document.getElementById('loginPassword').value
        };
        
        try {
            const response = await fetch(`${API_BASE_URL}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                // Store token in localStorage
                const token = data.token || getTokenFromCookie();
                if (!token) {
                    // If no token in response, try to get from cookie
                    showMessage('Login successful but token not received. Please try again.', 'error');
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Login';
                    return;
                }
                setToken(token);
                showDashboard(data.data);
                loginForm.reset();
            } else {
                showMessage(data.message, 'error');
            }
        } catch (error) {
            showMessage('Login failed. Please try again.', 'error');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Login';
        }
    });
}

// Helper to get token from cookie
function getTokenFromCookie() {
    const name = 'jwt_token=';
    const decodedCookie = decodeURIComponent(document.cookie);
    const ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return '';
}

// Check balance
if (checkBalanceBtn) {
    checkBalanceBtn.addEventListener('click', async () => {
        const token = getToken();
        
        checkBalanceBtn.disabled = true;
        checkBalanceBtn.innerHTML = '<span class="loading"></span>Fetching...';
        
        try {
            const response = await fetch(`${API_BASE_URL}/getBalance`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                balanceDisplay.textContent = `₹ ${data.data.balance.toLocaleString()}`;
                balanceDisplay.classList.add('balance-reveal');
                createConfetti();
            } else {
                showMessage(data.message, 'error');
                if (response.status === 401) {
                    removeToken();
                    setTimeout(() => {
                        window.location.reload();
                    }, 1500);
                }
            }
        } catch (error) {
            showMessage('Failed to fetch balance. Please try again.', 'error');
        } finally {
            checkBalanceBtn.disabled = false;
            checkBalanceBtn.textContent = 'Check Balance';
        }
    });
}

// Logout
if (logoutBtn) {
    logoutBtn.addEventListener('click', async () => {
        const token = getToken();
        
        if (token) {
            try {
                await fetch(`${API_BASE_URL}/logout`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
            } catch (error) {
                console.log('Logout error');
            }
        }
        
        removeToken();
        dashboardContainer.classList.add('hidden');
        loginContainer.classList.remove('hidden');
        loginForm.reset();
    });
}

// Confetti animation
function createConfetti() {
    const colors = ['#667eea', '#764ba2', '#f08c00', '#2f9e44', '#e03131', '#9c36b5'];
    const confettiCount = 100;
    
    for (let i = 0; i < confettiCount; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti';
        confetti.style.left = Math.random() * 100 + 'vw';
        confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        confetti.style.animationDuration = (Math.random() * 2 + 2) + 's';
        confetti.style.animationDelay = (Math.random() * 0.5) + 's';
        document.body.appendChild(confetti);
        
        setTimeout(() => {
            confetti.remove();
        }, 4000);
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
});
