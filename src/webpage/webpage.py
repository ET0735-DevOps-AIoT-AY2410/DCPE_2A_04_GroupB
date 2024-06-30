from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import logging

#To remote host:
#cd src
#python -m http.server

app = Flask(__name__)
CORS(app)

BASE_URL = 'http://127.0.0.1:5000'
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

namelist = []
booklist = {}

@app.route('/reserve', methods=['POST'])
def reserve():
    data = request.get_json()
    name = data.get('name')
    identity = data.get('identity')
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
