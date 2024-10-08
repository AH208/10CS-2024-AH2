from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import google.generativeai as genai
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Framework'

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

#   Create a connection to the SQLite3 database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

#   / = register
@app.route('/')
def home():
    return render_template('register.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    username = request.form['username']
    password = request.form['password']
    password = generate_password_hash(password)
    #   werkzueg password protection thing - Gives the users password a hashed password in database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # inserts the user details in the users table
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()  # commits the changes to the database
    conn.close()  # closes the connection to the database
    flash('User registered successfully!', 'success!')
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
#   werkzueg password protection thing - Checks if the users hashed password in database matches with input
    if user and check_password_hash(user[2], password):
        session['user'] = user[1]
        print(user)
        return redirect(url_for('account'))
    return redirect(url_for('login_fail'))


@app.route('/login_fail')
def login_fail():
    return render_template('login_fail.html')


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


@app.route('/account')
def account():
    if 'user' in session:
        user = session['user']
        return render_template('account.html', user=user)
    return redirect(url_for('login'))

#   TODO: settings might include image database - DO LAST
@app.route('/settings')
def settings():
    return render_template('settings.html')

#   Google Gemini AI is a cloud service not running on device
@app.route('/geminiai', methods=['GET', 'POST'])
def gemini():
    if "user" not in session:
        return redirect(url_for('login'))
    #   If user not logged in, redirect to log in
    prompt = ""
    output = ""
    if request.method == 'POST':
        prompt = request.form['input']
        output = model.generate_content(prompt).text
        #   connect database for recording input history
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        #   inserts the user details in the users table
        cursor.execute('INSERT INTO history (user_id, prompt, response) VALUES (?, ?, ?)', (session['user'], prompt, output))
        conn.commit()  # commits changes to the database
        conn.close()  # closes database connection

    return render_template('ai.html', input=prompt, output=output)


#   Log out route for button
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    get_db_connection()
    app.run(port=5000, debug=True)
