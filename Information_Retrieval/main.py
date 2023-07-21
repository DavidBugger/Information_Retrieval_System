from flask import Flask, render_template, request, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Set your own secret key

# Connect to the SQLite database
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

# Create the users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        details TEXT,
        criminal_offences TEXT
    )
''')
conn.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[2], password):
            session['username'] = user[1]
            session['role'] = user[3]
            flash('Login successful!', 'success')
            return redirect('/dashboard')
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect('/')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session or session['role'] != 'admin':
        flash('Unauthorized access!', 'error')
        return redirect('/')

    if request.method == 'POST':
        member_username = request.form['member_username']

        cursor.execute("SELECT * FROM users WHERE username = ?", (member_username,))
        member = cursor.fetchone()

        if member:
            return render_template('modal.html', member=member)
        else:
            flash('Member not found!', 'error')
    
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
