import sqlite3
from fastapi import FastAPI, Query, HTTPException
from typing import List, Dict, Any, Optional

# FastAPI app
app = FastAPI()

# Database connection
def get_db_connection():
    conn = sqlite3.connect('LRS.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/words", response_model=List[Dict[str, Any]])
async def get_words(
    page: int = Query(1, ge=1),
    sort_by: str = Query('kanji', enum=['kanji', 'romaji', 'english', 'correct_count', 'wrong_count']),
    order: str = Query('asc', enum=['asc', 'desc']),
    part_of_speech_id: Optional[int] = Query(None)  # New query parameter
):
    """
    Retrieve words with pagination, sorting, and optional part of speech filtering.

    - **page**: Page number (default: 1)
    - **sort_by**: Sort field (default: 'kanji')
    - **order**: Sort order (default: 'asc')
    - **part_of_speech_id**: Filter by part of speech ID (default: None)
    """
    conn = get_db_connection()
    offset = (page - 1) * 10  # Assuming 10 items per page
    order_clause = f"ORDER BY {sort_by} {order.upper()}"
    
    # Base query
    query = "SELECT * FROM words"
    
    # Add filtering for part of speech if specified
    if part_of_speech_id is not None:
        query += " WHERE part_of_speech_id = ?"
        words = conn.execute(query + f" {order_clause} LIMIT 10 OFFSET ?", (part_of_speech_id, offset)).fetchall()
    else:
        words = conn.execute(query + f" {order_clause} LIMIT 10 OFFSET ?", (offset,)).fetchall()
    
    conn.close()
    return [dict(word) for word in words]

@app.post("/groups")
def create_group(name: str):
    """
    Create a new word group.

    - **name**: Name of the group (required)
    
    Returns the created group's ID and name.
    """
    # Input validation
    if not name or not isinstance(name, str):
        raise HTTPException(status_code=400, detail="Group name is required and must be a string")
    
    # Database connection
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if group with this name already exists
        existing_group = cursor.execute("SELECT id FROM groups WHERE name = ?", (name,)).fetchone()
        if existing_group:
            raise HTTPException(status_code=400, detail=f"Group with name '{name}' already exists")
        
        # Insert new group
        cursor.execute("INSERT INTO groups (name, words_count) VALUES (?, 0)", (name,))
        conn.commit()
        
        # Get the ID of the newly created group
        group_id = cursor.lastrowid
        
        return {
            "id": group_id, 
            "name": name, 
            "words_count": 0
        }
    
    except sqlite3.Error as e:
        # Rollback in case of database error
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    finally:
        # Always close the connection
        conn.close()

@app.post("/study_sessions")
def create_study_session(group_id: int, study_activity_id: int):
    """
    Create a new study session for a group.

    - **group_id**: ID of the group to study (required)
    - **study_activity_id**: ID of the study activity (required)
    
    Returns the created study session's ID, group_id, and study_activity_id.
    """
    # Input validation
    if not group_id or not study_activity_id:
        raise HTTPException(status_code=400, detail="Both group_id and study_activity_id are required")
    
    # Database connection
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if group exists
        group = cursor.execute("SELECT id FROM groups WHERE id = ?", (group_id,)).fetchone()
        if not group:
            raise HTTPException(status_code=404, detail=f"Group with id {group_id} not found")
        
        # Check if study activity exists
        activity = cursor.execute("SELECT id FROM study_activities WHERE id = ?", (study_activity_id,)).fetchone()
        if not activity:
            raise HTTPException(status_code=404, detail=f"Study activity with id {study_activity_id} not found")
        
        # Insert new study session
        cursor.execute(
            "INSERT INTO study_sessions (group_id, study_activity_id) VALUES (?, ?)", 
            (group_id, study_activity_id)
        )
        conn.commit()
        
        # Get the ID of the newly created study session
        study_session_id = cursor.lastrowid
        
        return {
            "id": study_session_id, 
            "group_id": group_id, 
            "study_activity_id": study_activity_id
        }
    
    except sqlite3.Error as e:
        # Rollback in case of database error
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    finally:
        # Always close the connection
        conn.close()

# Run the app with: uvicorn main:app --reload