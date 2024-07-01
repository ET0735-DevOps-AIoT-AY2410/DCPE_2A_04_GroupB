from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import logging
import csv
import os

app = Flask(__name__)
CORS(app)

BASE_URL = 'http://127.0.0.1:5000'
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

booklist = {}
session = {}

def load_passwords():
    passwords = {}
    file_path = os.path.join(os.path.dirname(__file__), 'passwords.csv')
    print(file_path)
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            passwords[row['username']] = row['password']
    return passwords
    

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
        print(f'Session after login: {session}')
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Invalid identity or password'})

@app.route('/session', methods=['GET'])
def get_session():
    print(f'Session on /session request: {session}')
    if 'identity' in session:
        print("Session exists: TRUE")
        return jsonify({'loggedIn': True, 'identity': session['identity'], 'name': session['name']})
    else:
        print("Session exists: FALSE")
        return jsonify({'loggedIn': False})

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('identity', None)
    session.pop('name', None)
    print('Session after logout:', session)
    return jsonify({'success': True})

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
    booklist.setdefault(info, [])
    
    if len(booklist[info]) < 10:
        booklist[info].append([book_title, location, dateTime])
        print(booklist)
    else:
        return jsonify({'success': False})

    # Respond with a success message
    return jsonify({'success': True})

@app.route('/reservations', methods=['GET'])
def get_reservations():
    return jsonify(booklist)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
