const API_URL = 'http://localhost:8080';

window.addEventListener('DOMContentLoaded', () => {
    const user = getStoredUser();
    if (!user) {
        window.location.href = '/';
    }
});

function getStoredUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
}

async function handleUploadResume() {
    const file = document.getElementById('resumeFile').files[0];
    const text = document.getElementById('resumeText').value;
    
    let resumeText = text;
    
    if (file) {
        const reader = new FileReader();
        reader.onload = async (e) => {
            resumeText = e.target.result;
            await submitResume(resumeText);
        };
        reader.readAsText(file);
    } else if (text) {
        await submitResume(text);
    } else {
        document.getElementById('uploadError').textContent = 'Please select a file or paste text';
    }
}

async function submitResume(resumeText) {
    const user = getStoredUser();
    
    try {
        const response = await fetch(API_URL + '/api/uploadResume', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                userId: user.id,
                resumeText: resumeText
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Store resume ID and skills
            localStorage.setItem('currentResume', JSON.stringify({
                id: data.resumeId,
                skills: data.skills
            }));
            
            // Display skills
            displaySkills(data.skills);
        } else {
            document.getElementById('uploadError').textContent = 'Error uploading resume';
        }
    } catch (error) {
        document.getElementById('uploadError').textContent = 'Error: ' + error.message;
    }
}

function displaySkills(skills) {
    const skillsList = document.getElementById('skillsList');
    skillsList.innerHTML = '';
    
    if (Array.isArray(skills)) {
        skills.forEach(skill => {
            const tag = document.createElement('span');
            tag.className = 'skill-tag';
            tag.textContent = skill;
            skillsList.appendChild(tag);
        });
    }
    
    document.getElementById('skillsDisplay').style.display = 'block';
}

function startInterview() {
    window.location.href = '/interview.html';
}

function logout() {
    localStorage.removeItem('user');
    localStorage.removeItem('currentResume');
    location.href = '/';
}
