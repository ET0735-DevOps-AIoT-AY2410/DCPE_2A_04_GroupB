import readWriteBooks
import removeReserved
import calcFine
import userInfo

def update():
    data = readWriteBooks.loadBooks()
    removeReserved.checkReserveOver(data[0])

    fineList = calcFine.fining(data[1])
    userInfo.addFine(fineList)