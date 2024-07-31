import sys
sys.path.insert(0, './src')
print(sys.path)
import webpage.readWriteBooks as RWB

RWB.changeToReserve
RWB.loadBooks
RWB.removeBook

def test_loadBooks():
    expectedResult = ({}, {})
    result = RWB.loadBooks()
    assert(result == expectedResult)

def test_addBook():
    expectedResult = ({'pytester': [['testBook', 'Location 1', 'testReserveDate']]}, {})
    RWB.addBook('pytester', 'testBook', 'Location 1', 'testReserveDate')
    result = RWB.loadBooks()
    assert(result == expectedResult)


def test_changeToReserve():
    expectedResult = ({}, {'pytester': [['testBook', 'testBorrowDate']]})

    RWB.changeToReserve({'pytester': [['testBook', 'testBorrowDate']]})
    result = RWB.loadBooks()
    assert(result == expectedResult)

def test_removeBook():
    expectedResult = ({}, {})
    RWB.removeBook('pytester','testBook')
    result = RWB.loadBooks()
    assert(result == expectedResult)