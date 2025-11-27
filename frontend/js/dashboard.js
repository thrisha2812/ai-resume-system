const API_URL = 'http://localhost:8080';

window.addEventListener('DOMContentLoaded', () => {
    const user = getStoredUser();
    if (!user) {
        window.location.href = '/';
        return;
    }
    
    loadHistory();
});

function getStoredUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
}

async function loadHistory() {
    const user = getStoredUser();
    
    try {
        const response = await fetch(API_URL + '/api/history?userId=' + user.id);
        const data = await response.json();
        
        if (data.success) {
            displayHistory(data.history);
        }
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

function displayHistory(history) {
    const historyList = document.getElementById('historyList');
    
    if (!history || history.length === 0) {
        historyList.innerHTML = '<p class="no-data">No interview history yet. <a href="/interview.html">Start practicing!</a></p>';
        return;
    }
    
    historyList.innerHTML = '';
    
    let totalScore = 0;
    let maxScore = 0;
    
    history.forEach(item => {
        const date = new Date(item.date).toLocaleDateString();
        
        totalScore += item.score;
        maxScore = Math.max(maxScore, item.score);
        
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';
        historyItem.innerHTML = `
            <h4>Interview Session #${item.id}</h4>
            <div class="history-meta">
                <span>Score: <strong>${item.score}/100</strong></span>
                <span>Answers: ${item.answers}</span>
                <span>Date: ${date}</span>
            </div>
        `;
        historyList.appendChild(historyItem);
    });
    
    // Update stats
    document.getElementById('totalInterviews').textContent = history.length;
    document.getElementById('avgScore').textContent = Math.round(totalScore / history.length) + '%';
    document.getElementById('bestScore').textContent = maxScore + '%';
    
    if (history.length > 0) {
        const lastDate = new Date(history[0].date).toLocaleDateString();
        document.getElementById('lastInterview').textContent = lastDate;
    }
}

function logout() {
    localStorage.removeItem('user');
    location.href = '/';
}
