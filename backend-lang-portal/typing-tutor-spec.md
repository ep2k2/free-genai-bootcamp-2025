
# scope

i want to create a typing game as follows
- to run at the link Typing Tutor	http://localhost:8080 as specified in the study activities table
- to load all the words from a specified group
- show a start button which when clicked starts the game
- randomly select a kanji and have it slowly drift down from the top of the screen towards the bottom
- introduce a new kanji every 5 seconds
- match what the user types on the kyboard to the romaji of any kanji on the screen highlighting the kanji as it is matched
- remove any completely marched kanji from the screen
- include a score which starts at zero and increments each time a kanji is matched
- pause the game when any kanji reaches the bottom of the screen
- clear all kanjo from the screen and bring up the start button again

# technical spec
- simple prototype
- use API endpoints as defined in BACKEND_SPEC.md
- use uvicorn to run the server if possible
- use a browser to test the game
