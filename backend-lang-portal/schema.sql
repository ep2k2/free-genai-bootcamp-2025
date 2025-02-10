-- Created by Claude 3.5 from png image via Windsurf

-- Groups table
CREATE TABLE groups (
    id INT PRIMARY KEY,
    name STRING,
    words_count INT
);

-- Study Activities table
CREATE TABLE study_activities (
    id INT PRIMARY KEY,
    name STRING,
    url STRING
);

-- Words table
CREATE TABLE words (
    id INT PRIMARY KEY,
    kanji STRING,
    romaji STRING,
    english STRING,
    parts JSON
);

-- Study Sessions table
CREATE TABLE study_sessions (
    id INT PRIMARY KEY,
    group_id INT,
    study_activity_id INT,
    created_at TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES groups(id),
    FOREIGN KEY (study_activity_id) REFERENCES study_activities(id)
);

-- Word Groups junction table
CREATE TABLE word_groups (
    word_id INT,
    group_id INT,
    PRIMARY KEY (word_id, group_id),
    FOREIGN KEY (word_id) REFERENCES words(id),
    FOREIGN KEY (group_id) REFERENCES groups(id)
);

-- Word Review Items table
CREATE TABLE word_review_items (
    id INT PRIMARY KEY,
    word_id INT,
    study_session_id INT,
    correct BOOLEAN,
    created_at TIMESTAMP,
    FOREIGN KEY (word_id) REFERENCES words(id),
    FOREIGN KEY (study_session_id) REFERENCES study_sessions(id)
);
