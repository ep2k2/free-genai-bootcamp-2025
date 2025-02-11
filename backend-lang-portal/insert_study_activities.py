import json
import sqlite3

# Path to the JSON file
JSON_FILE_PATH = 'seeds/study_activities.json'

# Path to the SQLite database
DB_PATH = 'LRS.db'

def load_study_activities():
    # Read the JSON file
    with open(JSON_FILE_PATH, 'r') as file:
        study_activities = json.load(file)
    
    # Connect to the SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Insert each study activity
        for activity in study_activities:
            # Check if the activity already exists
            cursor.execute(
                "SELECT id FROM study_activities WHERE name = ? AND url = ?", 
                (activity['name'], activity['url'])
            )
            existing = cursor.fetchone()
            
            if not existing:
                # Insert new study activity
                cursor.execute(
                    "INSERT INTO study_activities (name, url) VALUES (?, ?)", 
                    (activity['name'], activity['url'])
                )
                print(f"Inserted study activity: {activity['name']}")
            else:
                print(f"Study activity already exists: {activity['name']}")
        
        # Commit the changes
        conn.commit()
        print("Study activities loaded successfully.")
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    
    finally:
        # Close the database connection
        conn.close()

if __name__ == "__main__":
    load_study_activities()
