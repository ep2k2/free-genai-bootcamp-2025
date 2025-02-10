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
