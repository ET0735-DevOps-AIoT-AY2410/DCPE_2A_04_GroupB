import requests

BASE_URL = 'http://192.168.50.191:5000'

def getReserve():
    try:
        url = f'{BASE_URL}/reservations'
        response = requests.get(url)
        bookList = response.json()
    except:
        return False
    
    return bookList

def main():
    print(getReserve())

if __name__ == '__main__':
    main()