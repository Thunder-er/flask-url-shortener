import sqlite3
import random
import string
from flask import Flask, render_template, request, redirect

# --- App Setup ---
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True # Good for development

# --- Helper Function ---
def get_db_connection():
    """Connects to the database."""
    conn = sqlite3.connect('urls.db')
    conn.row_factory = sqlite3.Row # Lets you access columns by name
    return conn

def generate_short_code(length=6):
    """Generates a random 6-character short code."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

# --- Routes ---

# Route 1: The main page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # User submitted the form
        original_url = request.form['url']
        short_code = generate_short_code()

        conn = get_db_connection()

        # Loop just in case the random code already exists (super rare)
        while True:
            try:
                conn.execute(
                    "INSERT INTO urls (short_code, original_url) VALUES (?, ?)",
                    (short_code, original_url)
                )
                conn.commit()
                break # Success!
            except sqlite3.IntegrityError:
                # 'UNIQUE' constraint failed. Generate a new code and try again.
                short_code = generate_short_code()
        conn.close()

        # Show the same page, but this time pass in the new short_url
        return render_template('index.html', short_url=short_code)

    # User just visited the page (GET request)
    return render_template('index.html')


# Route 2: The redirect
@app.route('/<short_code>')
def redirect_to_url(short_code):
    conn = get_db_connection()

    # Find the original URL that matches the short code
    url_row = conn.execute(
        "SELECT original_url FROM urls WHERE short_code = ?",
        (short_code,)
    ).fetchone()

    conn.close()

    if url_row:
        # If we found it, send the user there
        return redirect(url_row['original_url'])
    else:
        # If not, it's a 404
        return "URL not found", 404

# --- This makes `python app.py` work ---
if __name__ == "__main__":
    app.run(debug=True)