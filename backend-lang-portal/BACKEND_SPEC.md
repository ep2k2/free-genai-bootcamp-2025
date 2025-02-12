# Context

A language learning school wants to build a prototype of learning portal which will act as three things:
- Inventory of possible vocabulary that can be learned
- Act as a  Learning record store (LRS), providing correct and wrong score on practice vocabulary
- A unified launchpad to launch different learning apps


# Data model

Database tables to cover the following concepts:
- words (Kanji, Romaji, English, type, and an array of parts
- parts_of_speech (the type of word e.g. nonun, verb) #added from original design
- groups (a collection of words)
- word_groups (to join words and groups) 
- study_sessions (a session of study, including a group and an activity)
- word_review_items (an instance of a review on a word, in an activity, with its correct/incorrect boolean)
- study_activities (URLs to activities)

Store called LRS.db as strutured defined in schema.sql

Here is a summary of the data model:
words — Stores individual Japanese vocabulary words.
- `id` (Primary Key): Unique identifier for each word
- `kanji` (String, Required): The word written in Japanese kanji
- `romaji` (String, Required): Romanized version of the word
- `english` (String, Required): English translation of the word
- `parts` (JSON, Required): Word components stored in JSON format

parts_of_speech — Manages the different types of words.
- `id` (Primary Key): Unique identifier for each part of speech
- `type` (String, Required): The type of word (e.g., noun, verb, adjective)

groups — Manages collections of words.
- `id` (Primary Key): Unique identifier for each group
- `name` (String, Required): Name of the group
- `words_count` (Integer, Default: 0): Counter cache for the number of words in the group

word_groups — join-table enabling many-to-many relationship between words and groups.
- `word_id` (Foreign Key): References words.id
- `group_id` (Foreign Key): References groups.id

study_activities — Defines different types of study activities available.
- `id` (Primary Key): Unique identifier for each activity
- `name` (String, Required): Name of the activity (e.g., "Flashcards", "Quiz")
- `url` (String, Required): The full URL of the study activity

study_sessions — Records individual study sessions.
- `id` (Primary Key): Unique identifier for each session
- `group_id` (Foreign Key): References groups.id
- `study_activity_id` (Foreign Key): References study_activities.id
- `created_at` (Timestamp, Default: Current Time): When the session was created

word_review_items — Tracks individual word reviews within study sessions.
- `id` (Primary Key): Unique identifier for each review
- `word_id` (Foreign Key): References words.id
- `study_session_id` (Foreign Key): References study_sessions.id
- `correct` (Boolean, Required): Whether the answer was correct
- `created_at` (Timestamp, Default: Current Time): When the review occurred


# API definition

## words

GET /words - Get paginated list of words with review statistics
- **page**: Page number (default: 1, integer)
- **sort_by**: Sort field (default: 'kanji', options: 'kanji', 'romaji', 'english', 'id')
- **order**: Sort order (default: 'asc', options: 'asc', 'desc')
- **part_of_speech_id**: Filter by part of speech (default: None, integer)

Returns:
- List of words with their details
- Each word includes: id, kanji, romaji, english, parts

Possible Errors:
- 400 Bad Request: Invalid query parameters
- 500 Internal Server Error: Database-related issues


## groups

POST /groups - Create a new word group
- **name**: Name of the group (required, string)

Returns:
- **id**: Unique identifier of the created group
- **name**: Name of the group
- **words_count**: Initial count of words in the group (default: 0)

Possible Errors:
- 400 Bad Request: 
  - Missing or invalid group name
  - Group name already exists
- 500 Internal Server Error: Database-related issues


### GET /groups/{id}
- Retrieve details of a group by ID.
- Returns:
    - **id**: ID of the group
    - **name**: Name of the group
    - **words_count**: Number of words in the group
    - **words**: List of word IDs in the group

Possible Errors:
- 404 Not Found: Group does not exist
- 500 Internal Server Error: Database-related issues


### GET /groups/{id}/words
- Retrieve all details of words associated with a specific group by ID.
- Returns:
    - List of words with their details:
        - **id**: ID of the word
        - **kanji**: The kanji representation of the word
        - **romaji**: The romaji representation of the word
        - **english**: The English translation of the word

Possible Errors:
- 404 Not Found: Group does not exist
- 500 Internal Server Error: Database-related issues


## study sessions

### POST /study_sessions - Create a new study session
- **group_id**: ID of the group to study (required, integer)
- **study_activity_id**: ID of the study activity (required, integer)

Returns:
- **id**: Unique identifier of the created study session
- **group_id**: ID of the group studied
- **study_activity_id**: ID of the study activity used

Possible Errors:
- 400 Bad Request: Missing required parameters
- 404 Not Found: Group or study activity does not exist
- 500 Internal Server Error: Database-related issues

### POST /study_sessions/{id}/review - Log a review attempt for a word during a study session
- **id**: ID of the study session (required)
- **word_id**: ID of the word reviewed (required)
- **correct**: Whether the answer was correct (required)

Returns:
- **id**: Unique identifier of the review
- **word_id**: ID of the word reviewed
- **correct**: Whether the answer was correct

Possible Errors:
- 400 Bad Request: Missing required parameters
- 404 Not Found: Study session does not exist
- 500 Internal Server Error: Database-related issues


# Design constraint
- All tables use auto-incrementing primary keys
- Timestamps are automatically set on creation where applicable
- Foreign key constraints maintain referential integrity
- JSON storage for word parts allows flexible component storage
- Counter cache on groups.words_count optimizes word counting queries

# Protype allowances
- Backend is not validating inputs and trusting frontend
- No authentication or authorization
- Not good RESTful APIs (e.g. POST params in headers)
- No tests implemented :( #TODO
