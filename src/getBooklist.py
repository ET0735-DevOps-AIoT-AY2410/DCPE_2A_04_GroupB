import requests

def getReserve(BASE_URL):
    try:
        url = f'{BASE_URL}/reservations'
        response = requests.get(url)
        bookList = response.json()
    except:
        return [{}, {}]
    
    return bookList

def getFine(BASE_URL):
    try:
        url = f'{BASE_URL}/fines'
        response = requests.get(url)
        fineList = response.json()
    except:
        return [{}, {}]
    
    return fineList

def getUsers(BASE_URL):
    try:
        url = f'{BASE_URL}/users'
        response = requests.get(url)
        userList = response.json()
    except:
        return []
    
    return userList

def main():
    print(getReserve('http://192.168.50.191:5000'))
    print(getFine('http://192.168.50.191:5000'))

if __name__ == '__main__':
    main()