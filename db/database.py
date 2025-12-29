import os
from dotenv import load_dotenv

load_dotenv()  # loads from root .env by default

CONN_STR = os.getenv("CONN_STR")

def get_connection():
    import pyodbc
    if not CONN_STR:
        raise ValueError("Database connection string not found in environment variables")
    return pyodbc.connect(CONN_STR)
