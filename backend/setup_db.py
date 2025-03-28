import sqlite3

# Connect to SQLite
conn = sqlite3.connect("database/resumes.db")
cursor = conn.cursor()

# Create table for resumes
cursor.execute("""
    CREATE TABLE IF NOT EXISTS resumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        skills TEXT,
        text TEXT
    )
""")

conn.commit()
conn.close()

print("Database initialized successfully!")
