from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

namelist = []
booklist = {}

@app.route('/reserve', methods=['POST'])
def reserve():
    data = request.get_json()
    name = data.get('name')
    identity = data.get('identity')
    book_title = data.get('bookTitle')
    location = data.get('location')

    print(f'Reservation made by {name} ({identity}) for the book "{book_title}" at {location}')
    info = name + '&' + identity
    booklist.setdefault(info, [])
    
    if len(booklist[info]) < 10:
        booklist[info].append([book_title, location])
        print(booklist)
    
    else:
        return jsonify({'success': False})


    # Respond with a success message
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
