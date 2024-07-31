import time
from datetime import datetime, timedelta
import sys
sys.path.insert(0, './src/webpage')
print(sys.path)
import readWriteBooks as RWB
import removeReserved as removeReserved

def test_removeReserved_notOverdue():
    
    currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    RWB.addBook('pytester', 'testBook', 'Location 1', currentTime)
    expectedResult = ({'pytester': [['testBook', 'Location 1', currentTime]]}, {})

    removeReserved.checkReserveOver({'pytester': [['testBook', 'Location 1', currentTime]]})
    result = RWB.loadBooks()
    assert(expectedResult == result)
    RWB.removeBook('pytester','testBook')

def test_removeReserved_overdue():
    expectedResult = ({}, {})
    
    currentTime = datetime.now()
    currentTime = currentTime - timedelta(minutes=5)  
    currentTime = currentTime.strftime("%Y-%m-%d %H:%M:%S")

    RWB.addBook('pytester', 'testBook', 'Location 1', currentTime)

    removeReserved.checkReserveOver({'pytester': [['testBook', 'Location 1', currentTime]]})
    result = RWB.loadBooks()
    assert(expectedResult == result)