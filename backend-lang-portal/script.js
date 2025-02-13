let score = 0;
let kanjiArray = [];
let gameInterval;
let driftIntervals = []; // Array to hold all drift intervals

// Object to track the current input state for each kanji element
const currentInputState = {};

// Control variables
const initialKanjiDelay = 100; // Delay for the first kanji to appear (in milliseconds)
const subsequentKanjiDelay = 4000; // Delay for subsequent kanji (in milliseconds)
const driftSpeed = 0.025; // Time in seconds per pixel 0.025 good slow speed - increased to debug

// Function to start the game
function startGame() {
    score = 0;
    document.getElementById('score').innerText = 'Score: ' + score;
    document.getElementById('kanji-display').innerHTML = '';
    loadWords();
    document.getElementById('start-button').style.display = 'none'; // Hide the start button
    // Add keyboard event listener
    document.addEventListener('keydown', handleKeyPress);
}

// Function to start the game with a study session
function startGameWithSession(sessionId) {
    // Store the session ID for later use
    window.sessionId = sessionId; // Store it globally or in a suitable scope
    startGame(); // Call the existing startGame function
}

// Function to load words from a specified group
function loadWords() {
    fetch('/groups/5/words') // Update to use the correct endpoint - hard-coded for now to group=5 which is the test data set for typing tutor
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('API Response:', data); // Debug: Log the API response
            // Extract kanji and romaji from the response
            kanjiArray = data.map(item => {
                console.log('Processing item:', item); // Debug: Log each item
                return {
                    id: item.id, // Assuming the API returns an 'id' field
                    kanji: item.kanji, // Assuming the API returns a 'kanji' field
                    romaji: item.romaji // Assuming the API returns a 'romaji' field
                };
            });
            console.log('Processed kanjiArray:', kanjiArray); // Debug: Log the processed array
            // Call function to start displaying kanji
            animateKanji();
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

// Function to animate kanji falling down
function animateKanji() {
    // Keep a separate array for the original kanji data
    const originalKanjiArray = [...kanjiArray];
    
    // Function to get a random kanji from our loaded set
    function getRandomKanji() {
        return originalKanjiArray[Math.floor(Math.random() * originalKanjiArray.length)];
    }
    
    // Display first kanji after initial delay
    setTimeout(() => {
        displayKanji(getRandomKanji());
    }, initialKanjiDelay);
    
    // Set up interval to keep adding new kanji
    gameInterval = setInterval(() => {
        displayKanji(getRandomKanji());
    }, subsequentKanjiDelay);
}

// Function to display kanji on the screen
function displayKanji(kanji) {
    console.log('Displaying kanji object:', kanji);
    const kanjiDisplay = document.getElementById('kanji-display');
    const kanjiElement = document.createElement('div');
    kanjiElement.innerText = kanji.kanji;
    kanjiElement.classList.add('kanji');
    kanjiElement.dataset.id = kanji.id;
    // Generate a unique ID for this instance
    const instanceId = Date.now() + Math.random();
    kanjiElement.dataset.instanceId = instanceId;
    // Store the word ID directly on the element as well as in the input state
    kanjiElement.dataset.wordId = kanji.id;
    // Initialize input state for this instance
    currentInputState[instanceId] = { 
        romajiPointer: 0,
        kanji: kanji.kanji,
        romaji: kanji.romaji,
        wordId: kanji.id
    };
    console.log('Stored kanji ID in dataset:', kanjiElement.dataset.id);
    kanjiDisplay.appendChild(kanjiElement);

    // Randomize X position
    const randomX = Math.random() * (kanjiDisplay.clientWidth - 100);
    kanjiElement.style.position = 'absolute';
    kanjiElement.style.left = randomX + 'px';

    // Animate kanji drifting down
    let position = 0;
    const driftInterval = setInterval(() => {
        position += 1;
        kanjiElement.style.transform = 'translateY(' + position + 'px)';

        // Check if kanji reaches the bottom
        const kanjiDisplayHeight = kanjiDisplay.clientHeight;
        const kanjiHeight = kanjiElement.offsetHeight;
        if (position + kanjiHeight > kanjiDisplayHeight) {
            // End the game immediately
            clearInterval(driftInterval);
            clearInterval(gameInterval);
            driftIntervals.forEach(interval => clearInterval(interval));
            document.getElementById('start-button').style.display = 'block';
            document.removeEventListener('keydown', handleKeyPress);
            
            // Get word ID from either input state or element dataset
            const wordId = (currentInputState[instanceId] && currentInputState[instanceId].wordId) || 
                          kanjiElement.dataset.wordId;
            
            // Log failed review attempt if we have a word ID
            if (wordId) {
                logReviewAttempt(wordId, false);
            }
        }
    }, driftSpeed * 1000);

    // Store this interval
    driftIntervals.push(driftInterval);
}

function handleKeyPress(event) {
    const typedChar = event.key;
    const kanjiDisplay = document.getElementById('kanji-display');
    
    // Check each kanji element on screen
    Array.from(kanjiDisplay.children).forEach(element => {
        const instanceId = element.dataset.instanceId;
        const state = currentInputState[instanceId];
        
        if (state && state.romajiPointer < state.romaji.length) {
            if (typedChar === state.romaji[state.romajiPointer]) {
                // Advance the pointer
                state.romajiPointer++;
                if (state.romajiPointer === state.romaji.length) {
                    // Remove this instance of the kanji and increment score
                    element.remove();
                    score++;
                    document.getElementById('score').innerText = 'Score: ' + score;
                    
                    // Log successful review attempt
                    logReviewAttempt(state.wordId, true);
                    
                    delete currentInputState[instanceId];
                }
            } else {
                // Reset the pointer if the character does not match
                state.romajiPointer = 0;
            }
        }
    });
}

function logReviewAttempt(word_id, correct) {
    console.log('Attempting to log review with word_id:', word_id, 'correct:', correct);
    console.log('Request URL:', `/study_sessions/${window.sessionId}/review`);
    console.log('Request body:', { word_id, correct });
    
    fetch(`/study_sessions/${window.sessionId}/review`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            word_id: parseInt(word_id), // Ensure word_id is sent as an integer
            correct: Boolean(correct)    // Ensure correct is sent as a boolean
        }),
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => {
                console.error('Error response:', text);
                throw new Error('Network response was not ok');
            });
        }
        return response.json();
    })
    .then(data => {
        console.log('Review logged successfully:', data);
    })
    .catch(error => {
        console.error('Error logging review attempt:', error);
    });
}

// Event listener for start button
document.getElementById('start-button').addEventListener('click', () => startGameWithSession('2')); // test study_session id = 2 - in database this is for activity=1 "typing" using group 5 "test data"

// Show the button when the game is not running
document.getElementById('start-button').style.display = 'block';
