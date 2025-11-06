import sqlite3

print("Connecting to database...")
# This command creates 'urls.db' if it doesn't exist
conn = sqlite3.connect('urls.db')

# Create a cursor object to execute SQL
c = conn.cursor()

print("Creating table 'urls'...")
# This is the exact same SQL command from before
c.execute('''
CREATE TABLE urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    short_code TEXT NOT NULL UNIQUE,
    original_url TEXT NOT NULL
)
''')

# Save (commit) the changes and close the connection
conn.commit()
conn.close()

print("Done. Database 'urls.db' and table 'urls' created.")