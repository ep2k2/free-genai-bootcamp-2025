document.addEventListener('DOMContentLoaded', function() {
    // Initialize dashboard data
    fetchDashboardData();

    // Add event listeners for interactive elements
    setupEventListeners();
});

async function fetchDashboardData() {
    try {
        // Fetch all groups to get the most recent ones
        const groupsResponse = await fetch('/groups');
        if (!groupsResponse.ok) throw new Error('Failed to fetch groups');
        const groups = await groupsResponse.json();
        updateWordGroups(groups);

        // Fetch study sessions data
        const sessionsResponse = await fetch('/study_sessions');
        if (!sessionsResponse.ok) throw new Error('Failed to fetch sessions');
        const sessions = await sessionsResponse.json();
        
        // Sort sessions by creation time to get the most recent ones
        const sortedSessions = sessions.sort((a, b) => 
            new Date(b.created_at) - new Date(a.created_at)
        );

        if (sortedSessions.length > 0) {
            updateLastSession(sortedSessions[0]);
            updateRecentSessions(sortedSessions.slice(0, 5));
        }
    } catch (error) {
        console.error('Error fetching dashboard data:', error);
        showError('Failed to load dashboard data. Please try again later.');
    }
}

function updateLastSession(session) {
    if (!session) return;

    const lastSessionEl = document.getElementById('lastSession');
    
    // Get the study activity name
    fetch(`/study_activities/${session.study_activity_id}`)
        .then(response => response.json())
        .then(activity => {
            lastSessionEl.querySelector('.session-title').textContent = activity.name;
            lastSessionEl.querySelector('.session-timestamp').textContent = new Date(session.created_at).toLocaleString();
            
            // Count correct and incorrect answers
            fetch(`/study_sessions/${session.id}/reviews`)
                .then(response => response.json())
                .then(reviews => {
                    const correctCount = reviews.filter(review => review.correct).length;
                    const incorrectCount = reviews.filter(review => !review.correct).length;
                    
                    lastSessionEl.querySelector('.correct-count').textContent = correctCount;
                    lastSessionEl.querySelector('.incorrect-count').textContent = incorrectCount;
                })
                .catch(error => console.error('Error fetching session reviews:', error));
        })
        .catch(error => console.error('Error fetching activity details:', error));
}

function updateRecentSessions(sessions) {
    const sessionsList = document.getElementById('recentSessions');
    sessionsList.innerHTML = '';

    sessions.forEach(session => {
        // Get activity name for each session
        fetch(`/study_activities/${session.study_activity_id}`)
            .then(response => response.json())
            .then(activity => {
                const sessionEl = document.createElement('div');
                sessionEl.className = 'session-item';
                sessionEl.dataset.sessionId = session.id;
                sessionEl.innerHTML = `
                    <div class="session-title">${activity.name}</div>
                    <div class="session-timestamp">${new Date(session.created_at).toLocaleString()}</div>
                `;
                sessionEl.addEventListener('click', () => showSessionDetails(session));
                sessionsList.appendChild(sessionEl);
            })
            .catch(error => console.error('Error fetching activity details:', error));
    });
}

function updateWordGroups(groups) {
    const groupsList = document.getElementById('wordGroups');
    groupsList.innerHTML = '';

    groups.forEach(group => {
        const groupEl = document.createElement('div');
        groupEl.className = 'word-group-item';
        groupEl.dataset.groupId = group.id;
        groupEl.innerHTML = `
            <div class="group-name">${group.name}</div>
            <span class="word-count">${group.words_count} words</span>
        `;
        groupEl.addEventListener('click', () => showWordGroupDetails(group));
        groupsList.appendChild(groupEl);
    });
}

async function showSessionDetails(session) {
    try {
        const [activityResponse, reviewsResponse] = await Promise.all([
            fetch(`/study_activities/${session.study_activity_id}`),
            fetch(`/study_sessions/${session.id}/reviews`)
        ]);

        const activity = await activityResponse.json();
        const reviews = await reviewsResponse.json();

        const correctCount = reviews.filter(review => review.correct).length;
        const incorrectCount = reviews.filter(review => !review.correct).length;

        const detailsPanel = document.getElementById('detailsPanel');
        detailsPanel.querySelector('.details-content').innerHTML = `
            <h4>${activity.name}</h4>
            <p>Date: ${new Date(session.created_at).toLocaleString()}</p>
            <p>Correct Answers: ${correctCount}</p>
            <p>Incorrect Answers: ${incorrectCount}</p>
            <p>Total Reviews: ${reviews.length}</p>
            <p><a href="${activity.url}" target="_blank" class="btn btn-primary">Launch Activity</a></p>
        `;
    } catch (error) {
        console.error('Error fetching session details:', error);
        showError('Failed to load session details. Please try again later.');
    }
}

async function showWordGroupDetails(group) {
    try {
        const response = await fetch(`/groups/${group.id}/words`);
        if (!response.ok) throw new Error('Failed to fetch group words');
        const words = await response.json();

        const detailsPanel = document.getElementById('detailsPanel');
        detailsPanel.querySelector('.details-content').innerHTML = `
            <h4>${group.name}</h4>
            <p>Total Words: ${group.words_count}</p>
            <div class="word-list">
                ${words.map(word => `
                    <div class="word-item">
                        <span class="kanji">${word.kanji}</span>
                        <span class="romaji">${word.romaji}</span>
                        <span class="english">${word.english}</span>
                    </div>
                `).join('')}
            </div>
        `;
    } catch (error) {
        console.error('Error fetching group details:', error);
        showError('Failed to load group details. Please try again later.');
    }
}

function showError(message) {
    // Add error display logic here
    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-danger';
    errorDiv.textContent = message;
    document.querySelector('main').insertBefore(errorDiv, document.querySelector('main').firstChild);
    
    // Remove error after 5 seconds
    setTimeout(() => errorDiv.remove(), 5000);
}

function setupEventListeners() {
    // Add any global event listeners here
    document.addEventListener('click', function(e) {
        if (e.target.closest('.session-item')) {
            const sessionId = e.target.closest('.session-item').dataset.sessionId;
            fetch(`/study_sessions/${sessionId}`)
                .then(response => response.json())
                .then(session => showSessionDetails(session))
                .catch(error => {
                    console.error('Error fetching session:', error);
                    showError('Failed to load session details. Please try again later.');
                });
        }
        if (e.target.closest('.word-group-item')) {
            const groupId = e.target.closest('.word-group-item').dataset.groupId;
            fetch(`/groups/${groupId}`)
                .then(response => response.json())
                .then(group => showWordGroupDetails(group))
                .catch(error => {
                    console.error('Error fetching group:', error);
                    showError('Failed to load group details. Please try again later.');
                });
        }
    });
}
