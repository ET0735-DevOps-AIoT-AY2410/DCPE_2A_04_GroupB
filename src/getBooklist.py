import requests

def getReserve(BASE_URL):
    try:
        url = f'{BASE_URL}/reserve'
        response = requests.get(url, headers={'fromSite': 'true'})
        bookList = response.json()
    except:
        return [{}, {}]
    
    return bookList

def getFine(BASE_URL):
    try:
        url = f'{BASE_URL}/info'
        response = requests.get(url, headers={'fromSite': 'true', 'info': 'fine'})
        fineList = response.json()
    except:
        return [{}, {}]
    
    return fineList

def getUsers(BASE_URL):
    try:
        url = f'{BASE_URL}/info'
        response = requests.get(url, headers={'fromSite': 'true', 'info': 'user'})
        userList = response.json()
    except:
        return []
    
    return userList

def getDict(BASE_URL):
    try:
        url = f'{BASE_URL}/info'
        response = requests.get(url, headers={'fromSite': 'true', 'info': 'dictionary'})
        dictionary = response.json()
    except:
        return []
    
    return dictionary

def main():
    print(getReserve('http://192.168.50.191:5000'))
    print(getFine('http://192.168.50.191:5000'))

if __name__ == '__main__':
    main()