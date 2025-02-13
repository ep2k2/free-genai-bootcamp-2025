let score = 0;
let kanjiArray = [];
let gameInterval;
let driftIntervals = []; // Array to hold all drift intervals

// Object to track the current input state for each kanji
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
            // Initialize currentInputState after words are loaded
            kanjiArray.forEach(kanji => {
                currentInputState[kanji.kanji] = { romajiPointer: 0 };
            });
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
            // Stop this kanji's animation but do not remove it
            clearInterval(driftInterval);
            // Optionally, you can log a review attempt here if needed
            // logReviewAttempt(kanji.id, false); #TODO
        }
    }, driftSpeed * 1000);

    // Store this interval
    driftIntervals.push(driftInterval);
}

function handleKeyPress(event) {
    const typedChar = event.key;
    // Check each kanji on screen
    Object.keys(currentInputState).forEach(kanji => {
        const romaji = kanjiArray.find(k => k.kanji === kanji).romaji;
        const pointer = currentInputState[kanji].romajiPointer;

        if (pointer < romaji.length) {
            if (typedChar === romaji[pointer]) {
                // Advance the pointer
                currentInputState[kanji].romajiPointer++;
                if (currentInputState[kanji].romajiPointer === romaji.length) {
                    // Remove the kanji from display and increment score
                    removeKanji(kanji);
                    score++;
                    document.getElementById('score').innerText = 'Score: ' + score;
                    const wordId = kanjiArray.find(k => k.kanji === kanji).id; // Get the word_id
                    // logReviewAttempt(wordId, true); // Log success with the correct word_id # TODO
                }
            } else {
                // Reset the pointer if the character does not match
                currentInputState[kanji].romajiPointer = 0;
            }
        }
    });
}

function removeKanji(kanji) {
    // Logic to remove the kanji from the display
    const kanjiDisplay = document.getElementById('kanji-display');
    const kanjiElement = Array.from(kanjiDisplay.children).find(el => el.innerText === kanji);
    if (kanjiElement) {
        kanjiDisplay.removeChild(kanjiElement);
        delete currentInputState[kanji]; // Clean up the input state
    }
}

function logReviewAttempt(word_id, correct) {
    console.log('Attempting to log review with word_id:', word_id, 'correct:', correct); // Debug: Log the parameters
    console.log('Request URL:', `/study_sessions/${window.sessionId}/review`); // Debug: Log the URL
    console.log('Request body:', { word_id, correct }); // Debug: Log the request body
    fetch(`/study_sessions/${window.sessionId}/review`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            word_id: word_id,
            correct: correct, // Use the variable that indicates whether the answer was correct
        }),
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => {
                console.error('Error response:', text); // Debug: Log error response
                throw new Error('Network response was not ok');
            });
        }
        return response.json();
    })
    .then(data => {
        console.log('Review logged successfully:', data); // Debug: Log success response
    })
    .catch(error => {
        console.error('Error logging review attempt:', error);
    });
}

// Event listener for start button
document.getElementById('start-button').addEventListener('click', () => startGameWithSession('2')); // test study_session id = 2 - in database this is for activity=1 "typing" using group 5 "test data"

// Show the button when the game is not running
document.getElementById('start-button').style.display = 'block';
