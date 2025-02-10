import json
import sqlite3

# Connect to the LRS database
conn = sqlite3.connect('LRS.db')
cursor = conn.cursor()

# Load the JSON data
with open('starter files/data_verbs.json', 'r', encoding='utf-8') as file:
    verbs = json.load(file)

# Iterate over the verbs and insert them into the database
for verb in verbs:
    kanji = verb['kanji']
    romaji = verb['romaji']
    english = verb['english']
    part_of_speech_id = 1  # Adjective type

    # Insert the verb into the words table
    cursor.execute("INSERT INTO words (kanji, romaji, english, part_of_speech_id, parts) VALUES (?, ?, ?, ?, ?)", (kanji, romaji, english, part_of_speech_id, json.dumps(verb['parts'])))

# Commit the changes and close the connection
conn.commit()
conn.close()