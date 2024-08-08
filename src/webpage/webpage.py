from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
from datetime import datetime, timedelta
import logging
import userInfo
import readWriteBooks
from update import update
from calcFine import check_overdue_books
from dictionaryBooks import dictionary, libDict

import removeReserved
import calcFine

print(libDict)

app = Flask(__name__)
CORS(app, supports_credentials=True)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app.secret_key = 'super_secret_key'

BASE_URL = 'http://192.168.50.170:5001'

passwords = userInfo.load_passwords()

@app.route('/auth', methods=['POST'])
def login():
    if request.headers.get('fromSite') != 'true':
        return jsonify({'success': False, 'message': 'Unauthorised access'})
    
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

@app.route('/auth', methods=['DELETE'])
def logout():
    if request.headers.get('fromSite') != 'true':
        return jsonify({'success': False, 'message': 'Unauthorised access'})
    
    session.clear()
    return jsonify({'success': True})

@app.route('/auth', methods=['GET'])
def get_session():
    if request.headers.get('fromSite') != 'true':
        return jsonify({'success': False, 'message': 'Unauthorised access'})
    
    if 'identity' in session:
        return jsonify({'loggedIn': True, 'identity': session['identity'], 'name': session['name']})
    else:
        return jsonify({'loggedIn': False})

@app.route('/auth', methods=['PUT'])
def signup():
    if request.headers.get('fromSite') != 'true':
        return jsonify({'success': False, 'message': 'Unauthorised access'})
    
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
def add_reserve():
    if 'identity' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    if request.headers.get('fromSite') != 'true':
        return jsonify({'success': False, 'message': 'Unauthorised access'})

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

@app.route('/reserve', methods=['GET'])
def get_reservations():
    if request.headers.get('fromSite') != 'true':
        return jsonify({'success': False, 'message': 'Unauthorised access'})
    
    booklist = readWriteBooks.loadBooks()
    return jsonify(booklist)

@app.route('/reserve', methods=['DELETE'])
def cancel_reserve():
    if request.headers.get('fromSite') != 'true':
        return jsonify({'success': False, 'message': 'Unauthorised access'})
    
    data = request.get_json()
    info = data.get('info')
    bookId = data.get('bookId')
    readWriteBooks.removeBook(info, str(bookId))
    print(info, bookId)

    return jsonify({'success': True, 'message': 'Reservation cancelled successfully'})

@app.route('/info', methods=['GET'])
def books():
    update()
    if request.headers.get('fromSite') != 'true':
        return jsonify({'success': False, 'message': 'Unauthorised access'})
    
    if request.headers.get('info') == 'book':
        return jsonify(dictionary)
    
    elif request.headers.get('info') == 'fine':
        booklist = readWriteBooks.loadBooks()
        fineList = userInfo.loadFine()
        return jsonify([fineList, check_overdue_books(booklist[1])])
    
    elif request.headers.get('info') == 'user':
        userList = []
        for i in (userInfo.load_passwords().keys()):
            userList.append(i)

        return jsonify(userList)
    
    elif request.headers.get('info') == 'dictionary':
        userList = []

        return jsonify(libDict)
    
    else:
        return jsonify({'success': False, 'message': 'Error occurred'})

@app.route('/extendLoan', methods=['POST'])
def extendLoan():
    if request.headers.get('fromSite') != 'true':
        return jsonify({'success': False, 'message': 'Unauthorised access'})
    
    data = request.get_json()
    info = data.get('info')
    bookId = str(data.get('bookId'))
    borrowDate = data.get('borrowDate')

    borrowDate = datetime.strptime(borrowDate, '%Y-%m-%d %H:%M:%S')
    newDate = borrowDate + timedelta(minutes=7)
    newDate = datetime.strftime(newDate, '%Y-%m-%d %H:%M:%S') + 'E'    
    
    readWriteBooks.changeToReserve({info: [[bookId, newDate]]})

    return jsonify({'success': True, 'message': 'Loan extended successfully'})

@app.route('/return', methods=['POST'])
def returned():
    update()
    data = readWriteBooks.loadBooks()
    removeReserved.checkReserveOver(data[0])

    fineList = calcFine.fining(data[1])
    userInfo.addFine(fineList)
    
    if request.headers.get('info') == 'book':
        bookList = request.get_json()

        if len(bookList[list(bookList.keys())[0]][0]) == 2: #Test borrowed Book format
                readWriteBooks.changeToReserve(bookList)
    
        elif len(bookList) == 1: #Test returned book format
            for info in bookList:
                for book in bookList[info]:
                    readWriteBooks.removeBook(info, book[0])

        return jsonify({'success': True, 'message': 'Database edited'})
    
    elif request.headers.get('info') == 'fine':
        id = request.get_json()
        userInfo.addFine({id: 0})
        return jsonify({'success': True, 'message': 'Fine paid'})

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