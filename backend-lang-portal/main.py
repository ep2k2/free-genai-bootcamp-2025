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

def fetch_parts_of_speech_id(word_type: str) -> Optional[int]:
    """Fetch parts_of_speech_id based on word_type."""
    with db_connection() as conn:
        result = conn.execute("SELECT id FROM parts_of_speech WHERE type = ?", (word_type,)).fetchone()
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
    
    Fetches words with filtering by word type, sorting by one of the columns, and pagination.
    
    Args:
        page: Page number (starting from 1)
        sort_by: Column to sort by
        order: Sort order ('asc' or 'desc')
        word_type: Optional word type filter
        items_per_page: Number of items per page
    
    Returns:
        A list of dictionaries containing the fetched words.
    """
    # Establish a database connection using a context manager
    with db_connection() as conn:
        # Calculate the offset for pagination
        offset = (page - 1) * items_per_page
        
        # Initialize the base SQL query to select all columns from the words table
        query = ["SELECT * FROM words"]
        # Initialize an empty list for query parameters
        params: List[Any] = []
        
        # If a word type is specified, fetch its corresponding parts_of_speech_id
        if word_type:
            pos_result = fetch_parts_of_speech_id(word_type)
            if pos_result:
                # Append a WHERE clause to filter by type
                query.append("WHERE type = ?")
                # Add the type to the query parameters
                params.append(pos_result)
            else:
                # Return an empty list if the word type does not exist
                return []
        
        # Append an ORDER BY clause to sort the results
        query.append(f"ORDER BY {sort_by} {order.upper()}")
        # Append a LIMIT clause for pagination, specifying the number of items and offset
        query.append("LIMIT ? OFFSET ?")
        # Add items_per_page and offset to the query parameters
        params.extend([items_per_page, offset])
        
        # Execute the SQL query with the parameters and fetch all results

        print("Before fetching words")  # Debug statement
        words = conn.execute(" ".join(query), params).fetchall()
        print("After fetching words")  # Debug statement
        print(words)  # Debug statement

        # Convert the results to a list of dictionaries and return

        return [dict(word) for word in words]

def check_database_connection(db_file):
    try:
        # Attempt to connect to the SQLite database
        connection = sqlite3.connect(db_file)
        print("Database connection successful.")
        connection.close()
    except sqlite3.Error as e:
        print(f"Database connection failed: {e}")

# Call the function with the path to your SQLite database file
check_database_connection('lrs.db')

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