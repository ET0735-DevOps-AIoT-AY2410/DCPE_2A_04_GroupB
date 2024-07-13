import requests
import readWriteBooks
import time
import removeReserved

BASE_URL = 'http://192.168.50.170:5001'

def getReserve():
    try:
        url = f'{BASE_URL}'
        response = requests.get(url)
        bookList = response.json()

        if len(bookList[list(bookList.keys())[0]][0]) == 2: #Test borrowed Book format
            readWriteBooks.changeToReserve(bookList)
  
        elif len(bookList) == 1: #Test returned book format
            for info in bookList:
                for book in bookList[info]:
                    readWriteBooks.removeBook(info, book[0])

    except KeyboardInterrupt:
        exit()

    except:
        pass

    finally:
        reserveList = readWriteBooks.loadBooks()[0]
        removeReserved.checkReserveOver(reserveList)

def main():
    while(True):
        getReserve()
        time.sleep(1)

if __name__ == '__main__':
    main()