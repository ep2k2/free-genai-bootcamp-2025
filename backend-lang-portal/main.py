import sqlite3
from fastapi import FastAPI, Request, Query, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Dict, Any, Optional

# FastAPI app
app = FastAPI()
templates = Jinja2Templates(directory="/mnt/c/free-genai-bootcamp-2025/frontend-lang-portal/templates")

# Serve static files
app.mount("/static", StaticFiles(directory="backend-lang-portal"), name="static")

# Database connection
def get_db_connection():
    conn = sqlite3.connect('/mnt/c/free-genai-bootcamp-2025/backend-lang-portal/LRS.db')
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

@app.get("/groups/{id}")
def get_groups(id: int):
    """
    Retrieve details of a group by ID, including the group's name, word count, and a list of word IDs in the group.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch group details
    group = cursor.execute("SELECT id, name, words_count FROM groups WHERE id = ?", (id,)).fetchone()
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")

    # Fetch word IDs in the group
    words = cursor.execute("SELECT w.id FROM words w JOIN word_groups wg ON w.id = wg.word_id WHERE wg.group_id = ?", (id,)).fetchall()

    # Prepare response
    response = {
        "id": group[0],
        "name": group[1],
        "words_count": group[2],
        "words": [{"id": word[0]} for word in words]
    }

    return response

@app.get("/groups/{id}/words")
def get_group_words(id: int):
    """
    Retrieve all details of words associated with a specific group by ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch words in the group
    words = cursor.execute("SELECT w.id, w.kanji, w.romaji, w.english FROM words w JOIN word_groups wg ON w.id = wg.word_id WHERE wg.group_id = ?", (id,)).fetchall()

    if not words:
        raise HTTPException(status_code=404, detail="No words found for this group")

    # Prepare response
    response = [{"id": word[0], "kanji": word[1], "romaji": word[2], "english": word[3]} for word in words]

    return response

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

@app.get("/study_sessions", response_model=List[Dict[str, Any]])
async def get_study_sessions():
    """
    Retrieve a list of study sessions.

    Returns:
    - **id**: ID of the study session
    - **group_id**: ID of the group which was studied
    - **study_activity_id**: ID of the study activity used
    - **activity_name**: Name of the study activity
    - **created_at**: When the session was created
    """
    try:
        conn = get_db_connection()
        query = """
            SELECT 
                ss.id, 
                ss.group_id, 
                ss.study_activity_id,
                sa.name as activity_name,
                ss.created_at
            FROM study_sessions ss
            JOIN study_activities sa ON ss.study_activity_id = sa.id
            ORDER BY ss.created_at DESC
            LIMIT 5
        """
        sessions = conn.execute(query).fetchall()
        conn.close()
        return [dict(session) for session in sessions]
    except Exception as e:
        conn.close()  # Ensure the connection is closed on error
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/study_sessions/{id}", response_model=Dict[str, Any])
async def get_study_session(id: int):
    """
    Get the detail of reviews from a specific study session.

    Args:
    - **id**: ID of the study session

    Returns:
    - **id**: ID of the study session
    - **group_id**: ID of the group which was studied
    - **study_activity_id**: ID of the study activity used
    - **created_at**: When the session was created
    - **correct_count**: count of correct = true reviews from the session
    - **incorrect_count**: count of correct = false reviews from the session
    """
    try:
        conn = get_db_connection()
        
        # First get the session details
        session_query = """
            SELECT 
                ss.id,
                ss.group_id,
                ss.study_activity_id,
                ss.created_at,
                (SELECT COUNT(*) FROM word_review_items WHERE study_session_id = ss.id AND correct = 1) as correct_count,
                (SELECT COUNT(*) FROM word_review_items WHERE study_session_id = ss.id AND correct = 0) as incorrect_count
            FROM study_sessions ss
            WHERE ss.id = ?
        """
        
        session = conn.execute(session_query, (id,)).fetchone()
        
        if session is None:
            raise HTTPException(status_code=404, detail="Study session not found")
            
        conn.close()
        return dict(session)
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/study_sessions/{id}/review")
async def log_review_attempt(
    id: int,
    word_id: int,
    correct: bool
):
    """
    Log a review attempt for a word during a study session.

    - **id**: ID of the study session (required)
    - **word_id**: ID of the word reviewed (required)
    - **correct**: Whether the answer was correct (required)
    """
    # Input validation
    if not word_id:
        raise HTTPException(status_code=400, detail="word_id is required")

    # Database connection
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if study session exists
        session = cursor.execute("SELECT id FROM study_sessions WHERE id = ?", (id,)).fetchone()
        if not session:
            raise HTTPException(status_code=404, detail=f"Study session with id {id} not found")

        # Insert review attempt
        cursor.execute("INSERT INTO word_review_items (word_id, study_session_id, correct) VALUES (?, ?, ?)", (word_id, id, correct))
        conn.commit()

        return {
            "id": cursor.lastrowid,
            "word_id": word_id,
            "correct": correct
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# Run the app with: uvicorn main:app --reload