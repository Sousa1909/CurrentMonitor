import json
from app import app
from flask import Flask, request, session, redirect, url_for, render_template, jsonify
import hashlib
import json
from app import cLog

# Load users from the JSON file
with open('app/users.json', 'r') as f:
    users = json.load(f)

def check_password(username, password):
    if username in users:
        user = users[username]
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return password_hash == user['password_hash']
    return False

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cLog.info(users)
        if username in users and check_password(username, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return "Invalid credentials. Please try again."

    return render_template('login.html')

@app.route('/data_table')
def data_display():
    if 'username' in session:
        return render_template('data_table.html')
    else:
        return redirect(url_for('login'))
    

@app.route('/get_data')
def get_data():
    if 'username' in session:
        # Read the data from the JSON file
        with open('app/data/data.json', 'r') as file:
            data = json.load(file)
                # Reverse the order of the data to display the most recent entry on top
        reversed_data = list(reversed(data))
        return jsonify(reversed_data)
    else:
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))