import sqlite3
from fastapi import FastAPI, Query
from typing import List, Dict, Any

# FastAPI app
app = FastAPI()

# Database connection
def get_db_connection():
    conn = sqlite3.connect('lrs.db')
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

# Run the app with: uvicorn main:app --reload