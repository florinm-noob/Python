import sqlite3
import os
from contextlib import contextmanager
from .paths import DB_PATH, DATA_DIR
from .schema import create_tables

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

@contextmanager
def get_db_connection():
    """
    Context manager for SQLite database connection.
    Automatically commits or rolls back on exit.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")  # Enable foreign key constraints
    conn.row_factory = sqlite3.Row  # Enable column access by name
    try:
        yield conn
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def initialize_database():
    """
    Initialize the database with tables if they don't exist.
    """
    with get_db_connection() as conn:
        create_tables(conn)
        print("Database initialized successfully.")