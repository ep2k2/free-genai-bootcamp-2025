import sqlite3
from contextlib import contextmanager
from fastapi import FastAPI, Query
from typing import List, Dict, Any, Optional, Generator

app = FastAPI()

@contextmanager
def db_connection() -> Generator[sqlite3.Connection, None, None]:
    """Context manager for database connections."""
    conn = sqlite3.connect('lrs.db', check_same_thread=False)
    try:
        yield conn
    finally:
        conn.close()

def fetch_part_of_speech_id(word_type: str) -> Optional[int]:
    """Fetch part_of_speech_id based on word_type."""
    with db_connection() as conn:
        result = conn.execute("SELECT id FROM parts_of_speech WHERE type = ?", (wordtype,)).fetchone()
        return result[0] if result else None

def fetch_words(
    page: int = 1,
    sort_by: str = 'kanji',
    order: str = 'asc',
    word_type: Optional[str] = None,
    items_per_page: int = 10
) -> List[Dict[str, Any]]:
    """
    Fetch words with filtering, sorting, and pagination.
    
    Args:
        page: Page number (starting from 1)
        sort_by: Column to sort by
        order: Sort order ('asc' or 'desc')
        word_type: Optional word type filter
        items_per_page: Number of items per page
    """
    with db_connection() as conn:
        offset = (page - 1) * items_per_page
        query = ["SELECT * FROM words"]
        params: List[Any] = []
        
        if word_type:
            pos_result = fetch_part_of_speech_id(word_type)
            if pos_result:
                query.append("WHERE part_of_speech_id = ?")
                params.append(pos_result)
            else:
                return []
        
        query.append(f"ORDER BY {sort_by} {order.upper()}")
        query.append("LIMIT ? OFFSET ?")
        params.extend([items_per_page, offset])
        
        words = conn.execute(" ".join(query), params).fetchall()
        return [dict(word) for word in words]

@app.get("/words", response_model=List[Dict[str, Any]])
async def get_words(
    page: int = Query(1, ge=1),
    sort_by: str = Query('kanji', enum=['kanji', 'romaji', 'english', 'correct_count', 'wrong_count']),
    order: str = Query('asc', enum=['asc', 'desc']),
    word_type: Optional[str] = Query(None)
) -> List[Dict[str, Any]]:
    """
    Retrieve words with pagination, sorting, and optional word type filtering.

    Args:
        page: Page number (default: 1)
        sort_by: Sort field (default: 'kanji')
        order: Sort order (default: 'asc')
        word_type: Filter by word type (optional)
    """
    return fetch_words(page, sort_by, order, word_type)

# Run the app with: uvicorn main:app --reload