let score = 0;
let kanjiArray = [];
let gameInterval;
let driftIntervals = []; // Array to hold all drift intervals

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

// Function to start the game
function startGame() {
    score = 0;
    document.getElementById('score').innerText = 'Score: ' + score;
    document.getElementById('kanji-display').innerHTML = '';
    loadWords();
    document.getElementById('start-button').style.display = 'none'; // Hide the start button
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
    let currentKanjiIndex = 0;
    // Introduce the first kanji after 2 seconds
    setTimeout(() => {
        displayKanji(kanjiArray[currentKanjiIndex]);
        currentKanjiIndex++;
    }, 2000);
    gameInterval = setInterval(() => {
        if (currentKanjiIndex < kanjiArray.length) {
            const kanji = kanjiArray[currentKanjiIndex];
            displayKanji(kanji);
            currentKanjiIndex++;
        } else {
            clearInterval(gameInterval);
            // Reset the game or show end screen
            document.getElementById('start-button').style.display = 'block'; // Show the start button
        }
    }, 5000); // Introduce a new kanji every 5 seconds
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
        position += 2; // Move down
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
    }, 20);

    // Store this interval
    driftIntervals.push(driftInterval);
}

// Event listener for start button
document.getElementById('start-button').addEventListener('click', startGame);

// Show the button when the game is not running
document.getElementById('start-button').style.display = 'block';
