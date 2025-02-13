let score = 0;
let kanjiArray = [];
let gameInterval;
let driftIntervals = []; // Array to hold all drift intervals

// Object to track the current input state for each kanji
const currentInputState = {};

// TODO add keyboard matching to kanji romaji 
// - highlight component parts
// - when complete
//    remove element from display
//    increment score
//    PUT succesful review instance
            // POST /study_sessions/{id}/review - Log a review attempt for a word during a study session
            // - id: ID of the study session (required)
            // - word_id: ID of the word reviewed (required)
            // - correct: Whether the answer was correct (required)

// Control variables
const initialKanjiDelay = 100; // Delay for the first kanji to appear (in milliseconds)
const subsequentKanjiDelay = 4000; // Delay for subsequent kanji (in milliseconds)
const driftSpeed = 0.025; // Time in seconds per pixel

// Function to start the game
function startGame() {
    score = 0;
    document.getElementById('score').innerText = 'Score: ' + score;
    document.getElementById('kanji-display').innerHTML = '';
    kanjiArray.forEach(kanji => {
        currentInputState[kanji.kanji] = { romajiPointer: 0 }; // Initialize pointer for each kanji
    });
    loadWords();
    document.getElementById('start-button').style.display = 'none'; // Hide the start button
    // Add keyboard event listener
    document.addEventListener('keydown', handleKeyPress);
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
            // Extract kanji and romaji from the response
            kanjiArray = data.map(item => ({
                kanji: item.kanji, // Assuming the API returns a 'kanji' field
                romaji: item.romaji // Assuming the API returns a 'romaji' field
            }));
            // Call function to start displaying kanji
            animateKanji();
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

// Function to animate kanji falling down
function animateKanji() {
    kanjiArray.forEach((kanji, index) => {
        setTimeout(() => {
            displayKanji(kanji);
        }, index === 0 ? initialKanjiDelay : subsequentKanjiDelay * index);
    });
}

// Function to display kanji on the screen
function displayKanji(kanji) {
    const kanjiDisplay = document.getElementById('kanji-display');
    const kanjiElement = document.createElement('div');
    kanjiElement.innerText = kanji.kanji;
    kanjiElement.classList.add('kanji');
    kanjiDisplay.appendChild(kanjiElement);

    // Randomize X position
    const randomX = Math.random() * (kanjiDisplay.clientWidth - 50); // Adjust based on kanji width
    kanjiElement.style.position = 'absolute';
    kanjiElement.style.left = randomX + 'px';

    // Animate kanji drifting down
    let position = 0;
    const driftInterval = setInterval(() => {
        position += 1; // Move down one pixel
        kanjiElement.style.transform = 'translateY(' + position + 'px)';

        // Check if kanji reaches the bottom
        const kanjiDisplayHeight = kanjiDisplay.clientHeight;
        const kanjiHeight = kanjiElement.offsetHeight; // Get the height of the kanji element
        if (position + kanjiHeight > kanjiDisplayHeight) {
            clearInterval(driftInterval); // Stop this kanji's animation
            // Clear all drift intervals
            driftIntervals.forEach(interval => clearInterval(interval));
            clearInterval(gameInterval); // Stop the game
            // Record failed review instance
            // POST /study_sessions/{id}/review - Log a review attempt for a word during a study session
                // - id: ID of the study session (required)
                // - word_id: ID of the word reviewed (required)
                // - correct: Whether the answer was correct (required)
            document.getElementById('start-button').style.display = 'block'; // Show the start button
        }
    }, driftSpeed * 1000); // Convert seconds to milliseconds

    // Store this interval
    driftIntervals.push(driftInterval);
}

function handleKeyPress(event) {
    const typedChar = event.key;
    // Check each kanji on screen
    Object.keys(currentInputState).forEach(kanji => {
        const romaji = kanjiArray.find(k => k.kanji === kanji).romaji;
        const pointer = currentInputState[kanji].romajiPointer;

        // If the pointer is within the bounds of the romaji
        if (pointer < romaji.length) {
            if (typedChar === romaji[pointer]) {
                // Advance the pointer
                currentInputState[kanji].romajiPointer++;
                // Check if the end of the romaji is reached
                if (currentInputState[kanji].romajiPointer === romaji.length) {
                    // Remove the kanji from display and increment score
                    removeKanji(kanji);
                    score++;
                    document.getElementById('score').innerText = 'Score: ' + score;
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

// Event listener for start button
document.getElementById('start-button').addEventListener('click', startGame);

// Show the button when the game is not running
document.getElementById('start-button').style.display = 'block';
