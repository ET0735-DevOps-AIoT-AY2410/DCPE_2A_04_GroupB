import requests
import readWriteBooks
import time

BASE_URL = 'http://192.168.50.170:5001'

def getReserve():
    try:
        url = f'{BASE_URL}'
        response = requests.get(url)
        bookList = response.json()

        if len(bookList[list(bookList.keys())[0]][0]) == 2:
            readWriteBooks.changeToReserve(bookList)
        elif len(bookList) == 1:
            for info in bookList:
                for book in bookList[info]:
                    readWriteBooks.removeBook(info, book[0])

    except KeyboardInterrupt:
        exit()

    except:
        return [{}, {}]
    
    return bookList

def main():
    while(True):
        print(getReserve())
        time.sleep(1)

if __name__ == '__main__':
    main()