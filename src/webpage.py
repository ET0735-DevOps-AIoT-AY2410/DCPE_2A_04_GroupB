from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/reserve', methods=['POST'])
def reserve():
    data = request.get_json()
    name = data.get('name')
    identity = data.get('identity')
    book_title = data.get('bookTitle')
    location = data.get('location')

    # Print received data for debugging purposes
    print(f'Reservation made by {name} (Admin Number: {identity}) for the book "{book_title}" at "{location}"')

    # Respond with a success message
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
