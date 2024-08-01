import sys
sys.path.insert(0, './src/webpage')
print(sys.path)
import readWriteBooks as RWB

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