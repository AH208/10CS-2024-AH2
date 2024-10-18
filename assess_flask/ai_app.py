from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import google.generativeai as genai
import os
import requests
from dotenv import load_dotenv
#   Importation of needed libraries for flask, werkzeug, sqlite, gemini, os, requests, and the .env
#   style.css has preferred browser colour (Light/Dark mode)
#   And it also has resize of text area to vertical for the AI page

#   For the flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Framework'
#   Secret key

api_endpoint = 'http://localhost:11434/api/chat'
#   api_endpoint is a http due to https bringing an SSL issue

load_dotenv()
#   Google gemini has API key as an environment variable from a .env file to hide it from github.
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')


#   Create a connection to the SQLite3 database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
#   Rows = dictionaries
    return conn

#   Register
#   / = register
@app.route('/')
def home():
    return render_template('register.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register_post():
    #   Request username and password from registering user
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

#   Login

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    #   request the username and password from the logging in user
    username = request.form['username']
    password = request.form['password']
    #   database checking user info is correct
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    #   werkzueg password protection thing :/ - Checks if the users hashed password in database matches with input
    if user and check_password_hash(user[2], password):
        session['user'] = user[1]
        print(user)
        return redirect(url_for('homepage'))
    return redirect(url_for('login_fail'))

#   login_fail could have been a flash() but I used a html to try out w3 panels and stuff
@app.route('/login_fail')
def login_fail():
    return render_template('login_fail.html')

#   after login html pages

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


@app.route('/settings')
def settings():
    if 'user' in session:
        user = session['user']
        return render_template('settings.html', user=user)
#       user=user needed for {{ user }} to work
    return redirect(url_for('login'))
#   Redirect if not logged in

#   Artificial Intelligence
@app.route('/ai_page', defaults={'chat_id': None}, methods=['GET', 'POST'])
@app.route('/ai_page/<chat_id>', methods=['GET', 'POST'])
#   chat_id used for putting chats together into whole conversations with maybe context
def ai(chat_id):
    if "user" not in session:
        return redirect(url_for('login'))

    user_input = ""
    need_to_redirect = False
    model = "llama3"
#   default ai model is llama3

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    if not chat_id:
        #   if no chat_id it will create a new one by looking at the largest number in the database and +1ing it.
        cursor.execute('SELECT MAX(chat_id) FROM history')
        chat_id = cursor.fetchone()[0]+1
        need_to_redirect = True

#   Retrieving the chat history from the id and the end makes sure a user can't look at other users chat though chat_id
    cursor.execute('SELECT * FROM history WHERE chat_id = ? AND user_id = ?', (chat_id, session['user']))
    history = cursor.fetchall()
#   Retrieving the previous chat_ids for the logged-in user
    cursor.execute('SELECT distinct(chat_id) FROM history WHERE chat_id IS NOT NULL AND user_id = ?', (session['user'],))
    chats = cursor.fetchall()
    conn.close()  # closes database connection

#   If user posts to AI model, data will be sent to the AI model
    if request.method == 'POST':
        model = request.form.get('model')
        #   model request is in form of a button, input request is a typing input
        user_input = request.form['input']
        messages = []
        #   This loop format history for AI and NOT database
        for chat in history:
            user = chat[2]
            assistant = chat[3]
            messages.extend([{'role': 'user', 'content': user}, {'role': 'assistant', 'content': assistant}])
        #   Adds user input for the AI
        messages.append({'role': 'user', 'content': user_input})
        data = {
            'model': model,
            'stream': False,
            'messages': messages
        }
        #   Send to AI here
        ai_response = requests.post(api_endpoint, json=data)

#   200 means 'ok'
        if ai_response.status_code == 200:
            response_data = ai_response.json()
            assistant_response = response_data['message']['content']
            # messages.append(response_data['message'])

            #   connect database for recording input history
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            #   inserts a new chat message into the database
            row = (session['user'], user_input, assistant_response, model, chat_id)
            cursor.execute('INSERT INTO history (user_id, prompt, response, ai, chat_id) VALUES (?, ?, ?, ?, ?)',
                           row)
            #   displays last message in the box
            history.append((None,) + row)
            conn.commit()  # commits changes to the database
            conn.close()  # closes database connection
        else:
            print('Failed to get response from Ollama API')
        #   If else statement here to tell me if something goes wrong

    if need_to_redirect:
        return redirect(f"{url_for('ai')}/{chat_id}")
#   This redirects user to a new chat if user presses button

    last_chats = list(enumerate(chats, start=1))[-16:]
    #   numbers the chats then limits the previous chat button on the page to 16
    return render_template('ai_page.html', input=user_input, output=history, chats=last_chats, model=model)

#   Google Gemini AI is a cloud service not running on device
#   Reminder - homepage is also the page for Gemini AI
@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    #   If user not logged in, redirect to log in
    if "user" not in session:
        return redirect(url_for('login'))
    user = session['user']
    prompt = ""
    output = ""
    if request.method == 'POST':
        prompt = request.form['input']
        #   request form is a typing input for gemini and output from gemini is text.
        output = model.generate_content(prompt).text
        #   connect database for recording input history
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        #   inserts the user details in the users table
        cursor.execute('INSERT INTO history (user_id, prompt, response, ai) VALUES (?, ?, ?, ?)',
                       (session['user'], prompt, output, "gemini"))
        conn.commit()  # commits changes to the database
        conn.close()  # closes database connection

    return render_template('home_page.html', input=prompt, output=output , user=user)


#   Log out route for button
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    get_db_connection()
    app.run(port=5000, debug=True)

#           Register
#   Login  -|
#           Home_page
#               \
#                AI page AND Settings
