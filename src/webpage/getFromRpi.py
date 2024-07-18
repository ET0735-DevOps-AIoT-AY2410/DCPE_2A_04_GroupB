import requests
import time

import readWriteBooks
import removeReserved
import calcFine
import userPasswordFine

def getReserve(BASE_URL):
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

    try:
        url = f'{BASE_URL}/finepaid'
        response = requests.get(url)
        id = response.json()
        userPasswordFine.addFine({id: 0})

    except:
        pass

    finally:
        data = readWriteBooks.loadBooks()
        removeReserved.checkReserveOver(data[0])

        fineList = calcFine.fining(data[1])
        userPasswordFine.addFine(fineList)

def main():
    while(True):
        getReserve('http://192.168.50.170:5001')
        time.sleep(1)

if __name__ == '__main__':
    main()