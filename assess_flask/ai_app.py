from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'FrameworkRyzen7040'

#   Create a connection to the SQLite3 database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def home():
    return render_template('register.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    age = request.form['age']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # inserts the user details in the users table
    cursor.execute('INSERT INTO users (username, password, age) VALUES (?, ?, ?)', (username, password, age))
    conn.commit()  # commits the changes to the database
    conn.close()  # closes the connection to the database
    flash('User registered successfully!', 'success!')
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['user'] = user[1]
        print(user)
        session['age'] = user[3]
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
        age = session['age']
        return render_template('account.html', user=user, age=age)
    return redirect(url_for('login'))


#   Log out Route
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('age', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    get_db_connection()
    app.run(port=5000, debug=True)
