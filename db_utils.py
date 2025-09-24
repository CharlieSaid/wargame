"""
Shared database utilities for the wargame application.
Centralizes database connection and query execution.
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables once
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    """Create a new database connection with RealDictCursor"""
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable not found")
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def execute_sql(sql, params=None, fetch_one=False, fetch_all=False, error_message=None):
    """
    Execute a database query with proper connection management
    
    Args:
        sql: SQL query string
        params: Query parameters tuple
        fetch_one: Return single row
        fetch_all: Return all rows
        error_message: Custom error message for logging
    
    Returns:
        Query result or number of affected rows
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                
                if fetch_one:
                    return cursor.fetchone()
                elif fetch_all:
                    return cursor.fetchall()
                else:
                    conn.commit()
                    return cursor.rowcount
    except Exception as e:
        if error_message:
            print(f"{error_message}: {e}")
        else:
            print(f"Database error: {e}")
        return None
