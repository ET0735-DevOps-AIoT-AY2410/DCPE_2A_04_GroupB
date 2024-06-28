import requests

BASE_URL = 'http://127.0.0.1:5000'

def get_reservations():
    url = f'{BASE_URL}/reservations'
    response = requests.get(url)
    print('All reservations:', response.json())
    bookList = response.json()
    
    return bookList

def main():
    print(get_reservations())

if __name__ == '__main__':
    main()