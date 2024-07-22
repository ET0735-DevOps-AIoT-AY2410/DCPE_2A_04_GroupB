import requests

BASE_URL = 'http://192.168.50.191:5000'

def getReserve():
    try:
        url = f'{BASE_URL}/reservations'
        response = requests.get(url)
        bookList = response.json()
    except:
        return [{}, {}]
    
    return bookList

def getFine():
    try:
        url = f'{BASE_URL}/fines'
        response = requests.get(url)
        fineList = response.json()
    except:
        return [{}, {}]
    
    return fineList

def main():
    print(getReserve())
    print(getFine())

if __name__ == '__main__':
    main()