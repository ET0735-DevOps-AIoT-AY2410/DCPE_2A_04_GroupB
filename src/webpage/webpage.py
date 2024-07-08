from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
from datetime import datetime, timedelta
import logging
import csv
import os
import readWriteBooks
from threading import Thread
import requests

app = Flask(__name__)
CORS(app, supports_credentials=True)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app.secret_key = 'super_secret_key'

def load_passwords():
    passwords = {}
    file_path = os.path.join(os.path.dirname(__file__), 'passwords.csv')
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            passwords[row['username']] = row['password']
    return passwords

def createAcc(username, password):
    global passwords
    file_path = os.path.join(os.path.dirname(__file__), 'passwords.csv')
    with open(file_path, 'a', newline='') as csvfile:
        fieldnames = ['username', 'password']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow({'username': username, 'password': password})
    
    passwords = load_passwords()

passwords = load_passwords()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    identity = data.get('identity')
    password = data.get('password')
    user = data.get('user')
    
    if identity in passwords and passwords[identity] == password:
        session['identity'] = identity
        session['name'] = user
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Invalid identity or password'})

@app.route('/session', methods=['GET'])
def get_session():
    if 'identity' in session:
        return jsonify({'loggedIn': True, 'identity': session['identity'], 'name': session['name']})
    else:
        return jsonify({'loggedIn': False})

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    identity = data.get('identity')
    password = data.get('password')

    if identity in passwords:
        return jsonify({'success': False, 'message': 'Admin No. already used'})
    
    createAcc(identity, password)
    passwords[identity] = password
    return jsonify({'success': True, 'message': 'Account created successfully'})

@app.route('/reserve', methods=['POST'])
def reserve():
    if 'identity' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})

    data = request.get_json()
    name = data.get('name')
    identity = session['identity']
    book_title = data.get('bookTitle')
    location = data.get('location')
    reserveTime = data.get('reserveTime')

    reserveDate = datetime.fromisoformat(reserveTime.replace('Z', '+00:00')) + timedelta(hours=8)
    dateTime = reserveDate.strftime('%Y-%m-%d %H:%M:%S')

    print(f'Reservation made by {name} ({identity}) for the book "{book_title}" at {location}, {dateTime}')
    info = name + '&' + identity

    booklist = readWriteBooks.loadBooks()
    if info not in booklist or len(booklist[info]) <= 10:
        readWriteBooks.addBook(info, book_title, location, dateTime)

    return jsonify({'success': True})

@app.route('/reservations', methods=['GET'])
def get_reservations():
    booklist = readWriteBooks.loadBooks()
    print(booklist)
    return jsonify(booklist)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_account')
def create_account():
    return render_template('createAcc.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
