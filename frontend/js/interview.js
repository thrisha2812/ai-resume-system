const API_URL = 'http://localhost:8080';

let currentSession = null;
let currentQuestion = 0;
let totalQuestions = 5;
let scores = [];

// Load previous session if exists
window.addEventListener('DOMContentLoaded', () => {
    const user = getStoredUser();
    if (!user) {
        window.location.href = '/';
        return;
    }

    const session = localStorage.getItem('currentSession');
    if (session) {
        currentSession = JSON.parse(session);
        showSection('questionSection');
        loadNextQuestion();
    }
});

function getStoredUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
}

async function startNewInterview() {
    const user = getStoredUser();
    const resume = localStorage.getItem('currentResume');
    
    if (!resume) {
        alert('Please upload your resume first');
        window.location.href = '/upload.html';
        return;
    }

    const resumeData = JSON.parse(resume);

    // FIX: Prevent undefined skills
    if (!resumeData.skills || resumeData.skills.length === 0) {
        alert("No skills detected from resume. Please upload again.");
        return;
    }

    try {
        const response = await fetch(API_URL + '/api/startInterview', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                userId: user.id,
                skills: resumeData.skills   // FIXED (removed JSON.stringify)
            })
        });

        const data = await response.json();

        if (!data.success) {
            alert(data.message || 'Failed to start interview.');
            return;
        }

        // Update values
        currentSession = {
            id: data.sessionId,
            skills: resumeData.skills
        };
        currentQuestion = 0;
        scores = [];

        // If backend sends total questions
        if (data.totalQuestions) totalQuestions = data.totalQuestions;

        localStorage.setItem('currentSession', JSON.stringify(currentSession));

        showSection('questionSection');
        displayQuestion(data.question);

    } catch (error) {
        alert('Error starting interview: ' + error.message);
    }
}

async function loadNextQuestion() {
    if (!currentSession) {
        alert("Session expired. Start again.");
        window.location.href = '/dashboard.html';
        return;
    }

    if (currentQuestion >= totalQuestions) {
        completeInterview();
        return;
    }

    try {
        const response = await fetch(API_URL + '/api/nextQuestion', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                sessionId: currentSession.id,
                skills: currentSession.skills,     // FIXED
                questionCount: currentQuestion
            })
        });

        const data = await response.json();

        if (!data.success) {
            alert(data.message || 'Could not load next question');
            return;
        }

        displayQuestion(data.question);

    } catch (error) {
        alert('Error loading question: ' + error.message);
    }
}

function displayQuestion(question) {
    document.getElementById('questionText').textContent = question;
    document.getElementById('answerText').value = '';
    document.getElementById('questionCounter').textContent =
        `Question ${currentQuestion + 1}/${totalQuestions}`;

    const progress = ((currentQuestion + 1) / totalQuestions) * 100;
    document.getElementById('progressFill').style.width = progress + '%';
}

async function submitAnswer() {
    const question = document.getElementById('questionText').textContent;
    const answer = document.getElementById('answerText').value;

    if (!answer.trim()) {
        alert('Please provide an answer');
        return;
    }

    try {
        const response = await fetch(API_URL + '/api/evaluateAnswer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                sessionId: currentSession.id,
                question: question,
                answer: answer
            })
        });

        const data = await response.json();

        if (!data.success) {
            alert(data.message || 'Evaluation failed');
            return;
        }

        scores.push(data.score);

        // Show feedback
        document.getElementById('scoreNumber').textContent = data.score;
        document.getElementById('feedbackText').textContent = data.feedback;

        currentQuestion++;
        showSection('feedbackSection');

    } catch (error) {
        alert('Error evaluating answer: ' + error.message);
    }
}

async function nextQuestion() {
    if (currentQuestion < totalQuestions) {
        showSection('questionSection');
        loadNextQuestion();
    } else {
        completeInterview();
    }
}

function completeInterview() {
    const avgScore =
        scores.length > 0 ? Math.round(scores.reduce((a, b) => a + b) / scores.length) : 0;

    document.getElementById('finalScore').textContent = avgScore + '/100';

    let message = '';
    if (avgScore >= 80) {
        message = 'Excellent performance! You\'re well-prepared for interviews.';
    } else if (avgScore >= 60) {
        message = 'Good effort! Keep practicing to improve your interview skills.';
    } else {
        message = 'Keep practicing! Review these topics and try again.';
    }

    document.getElementById('completionMessage').textContent = message;

    showSection('completionSection');
}

async function saveProgress() {
    const user = getStoredUser();
    const avgScore =
        scores.length > 0 ? Math.round(scores.reduce((a, b) => a + b) / scores.length) : 0;

    try {
        const response = await fetch(API_URL + '/api/saveProgress', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                userId: user.id,
                sessionId: currentSession.id,
                score: avgScore
            })
        });

        const data = await response.json();

        if (!data.success) {
            alert(data.message || 'Saving progress failed');
            return;
        }

        localStorage.removeItem('currentSession');
        alert('Progress saved successfully!');
        window.location.href = '/dashboard.html';

    } catch (error) {
        alert('Error saving progress: ' + error.message);
    }
}

function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(el => {
        el.style.display = 'none';
    });
    document.getElementById(sectionId).style.display = 'block';
}

function logout() {
    localStorage.removeItem('user');
    localStorage.removeItem('currentSession');
    location.href = '/';
}
