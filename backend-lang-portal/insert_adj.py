import json
import sqlite3

# Connect to the LRS database
conn = sqlite3.connect('LRS.db')
cursor = conn.cursor()

# Load the JSON data
with open('starter files/data_adjectives.json', 'r', encoding='utf-8') as file:
    adjs = json.load(file)

# Iterate over the adjs and insert them into the database
for adj in adjs:
    kanji = adj['kanji']
    romaji = adj['romaji']
    english = adj['english']
    part_of_speech_id = 1  # Adjective type

    # Insert the adj into the words table
    cursor.execute("INSERT INTO words (kanji, romaji, english, part_of_speech_id, parts) VALUES (?, ?, ?, ?, ?)", (kanji, romaji, english, part_of_speech_id, json.dumps(adj['parts'])))

# Commit the changes and close the connection
conn.commit()
conn.close()