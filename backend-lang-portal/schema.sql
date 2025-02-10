-- Created by Claude 3.5 from png image via Windsurf -- edited to include parts_of_speech

-- Groups table
CREATE TABLE groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name STRING,
    words_count INT DEFAULT 0
);

-- Study Activities table
CREATE TABLE study_activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name STRING,
    url STRING
);

-- Study Sessions table
CREATE TABLE study_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id INT,
    study_activity_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES groups(id),
    FOREIGN KEY (study_activity_id) REFERENCES study_activities(id)
);

-- Word Groups table
CREATE TABLE word_groups (
    word_id INT,
    group_id INT,
    PRIMARY KEY (word_id, group_id),
    FOREIGN KEY (word_id) REFERENCES words(id),
    FOREIGN KEY (group_id) REFERENCES groups(id)
);

-- Word Review Items table
CREATE TABLE word_review_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_id INT,
    study_session_id INT,
    correct BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (word_id) REFERENCES words(id),
    FOREIGN KEY (study_session_id) REFERENCES study_sessions(id)
);

-- Parts of Speech table
CREATE TABLE parts_of_speech (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type STRING NOT NULL
);

-- Words table
CREATE TABLE IF NOT EXISTS "words" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kanji STRING,
    romaji STRING,
    english STRING,
    parts JSON,
    part_of_speech_id INT,
    FOREIGN KEY (part_of_speech_id) REFERENCES parts_of_speech(id),
);
