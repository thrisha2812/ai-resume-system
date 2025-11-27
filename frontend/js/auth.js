const API_URL = 'http://localhost:8080';

// Check authentication on page load
window.addEventListener('DOMContentLoaded', () => {
    const user = getStoredUser();
    if (user) {
        showMainSection();
    } else {
        showAuthSection();
    }
});

function showTab(tab) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-button').forEach(el => el.classList.remove('active'));
    
    document.getElementById(tab + 'Tab').classList.add('active');
    event.target.classList.add('active');
    
    document.getElementById('loginError').textContent = '';
    document.getElementById('signupError').textContent = '';
}

async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    
    try {
        const response = await fetch(API_URL + '/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (data.success) {
            storeUser(data.userId, data.name, email);
            showMainSection();
        } else {
            document.getElementById('loginError').textContent = 'Invalid email or password';
        }
    } catch (error) {
        document.getElementById('loginError').textContent = 'Error: ' + error.message;
    }
}

async function handleSignup(e) {
    e.preventDefault();
    const name = document.getElementById('signupName').value;
    const email = document.getElementById('signupEmail').value;
    const password = document.getElementById('signupPassword').value;
    const confirm = document.getElementById('signupConfirm').value;
    
    if (password !== confirm) {
        document.getElementById('signupError').textContent = 'Passwords do not match';
        return;
    }
    
    try {
        const response = await fetch(API_URL + '/api/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, password })
        });
        
        const data = await response.json();
        
        if (data.success) {
            storeUser(null, name, email);
            // Auto-login
            handleLogin({ preventDefault: () => {} });
        } else {
            document.getElementById('signupError').textContent = 'User already exists';
        }
    } catch (error) {
        document.getElementById('signupError').textContent = 'Error: ' + error.message;
    }
}

function storeUser(userId, name, email) {
    const user = { id: userId || Date.now(), name, email };
    localStorage.setItem('user', JSON.stringify(user));
    updateNavigation(true);
}

function getStoredUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
}

function logout() {
    localStorage.removeItem('user');
    localStorage.removeItem('currentSession');
    location.href = '/';
}

function showAuthSection() {
    if (document.getElementById('authSection')) {
        document.getElementById('authSection').style.display = 'block';
        document.getElementById('mainSection').style.display = 'none';
        updateNavigation(false);
    }
}

function showMainSection() {
    if (document.getElementById('mainSection')) {
        document.getElementById('authSection').style.display = 'none';
        document.getElementById('mainSection').style.display = 'block';
        updateNavigation(true);
    }
}

function updateNavigation(isLoggedIn) {
    const navHome = document.getElementById('navHome');
    const navDashboard = document.getElementById('navDashboard');
    const navLogout = document.getElementById('navLogout');
    const navLogin = document.getElementById('navLogin');
    
    if (navHome) {
        navHome.style.display = isLoggedIn ? 'inline' : 'none';
    }
    if (navDashboard) {
        navDashboard.style.display = isLoggedIn ? 'inline' : 'none';
    }
    if (navLogout) {
        navLogout.style.display = isLoggedIn ? 'inline' : 'none';
        navLogout.onclick = logout;
    }
    if (navLogin) {
        navLogin.style.display = isLoggedIn ? 'none' : 'inline';
    }
}

function navigateTo(path) {
    const user = getStoredUser();
    if (user) {
        window.location.href = path;
    } else {
        alert('Please login first');
    }
}
