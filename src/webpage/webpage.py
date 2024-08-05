from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
from datetime import datetime, timedelta
import logging
import userInfo
import readWriteBooks
from getFromRpi import getReserve
from calcFine import check_overdue_books

app = Flask(__name__)
CORS(app, supports_credentials=True)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app.secret_key = 'super_secret_key'

BASE_URL = 'http://192.168.50.170:5001'

passwords = userInfo.load_passwords()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    name = str(data.get('user'))
    admNo = str(data.get('identity'))
    identity = name + '&' + admNo
    password = data.get('password')
    user = data.get('user')
    
    if identity in passwords and passwords[identity] == password:
        session['identity'] = admNo
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
    global passwords
    data = request.get_json()
    name = str(data.get('user'))
    admNo = str(data.get('identity'))
    identity = name + '&' + admNo
    password = data.get('password')

    if identity in passwords:
        return jsonify({'success': False, 'message': 'Admin No. already used'})
    
    userInfo.createAcc(identity, password) 
    passwords = userInfo.load_passwords()
    passwords[identity] = password
    return jsonify({'success': True, 'message': 'Account created successfully'})

@app.route('/reserve', methods=['POST'])
def reserve():
    if 'identity' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})

    data = request.get_json()
    name = data.get('name')
    identity = session['identity']
    bookID = data.get('bookID')
    book_title = data.get('bookTitle')
    location = data.get('location')
    reserveTime = data.get('reserveTime')

    reserveDate = datetime.fromisoformat(reserveTime.replace('Z', '+00:00')) + timedelta(hours=8)
    dateTime = reserveDate.strftime('%Y-%m-%d %H:%M:%S')

    print(f'Reservation made by {name} ({identity}) for the book "{book_title}"({bookID}) at {location}, {dateTime}')
    info = name + '&' + identity

    booklist = readWriteBooks.loadBooks()
    if info not in booklist or len(booklist[info]) <= 10:
        readWriteBooks.addBook(info, bookID, location, dateTime)

    return jsonify({'success': True})

@app.route('/reservations', methods=['GET'])
def get_reservations():
    booklist = readWriteBooks.loadBooks()
    return jsonify(booklist)

@app.route('/users', methods=['GET'])
def getUsers():
    userList = []
    for i in (userInfo.load_passwords().keys()):
        userList.append(i)

    return jsonify(userList)

@app.route('/fines', methods=['GET'])
def get_fines():
    getReserve(BASE_URL)
    booklist = readWriteBooks.loadBooks()
    fineList = userInfo.loadFine()
    return jsonify([fineList, check_overdue_books(booklist[1])])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_account')
def create_account():
    return render_template('createAcc.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/reserved')
def reserved():
    return render_template('reserved.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)