import sys
sys.path.insert(0, './src/webpage')
print(sys.path)
from parseDateTime import getYear, getMonth, getDay, getHour, getMin, getSec

testDateTime = '2024-06-09 02:18:29'

def test_getYear():
    expected_getYear='2024'
    assert(getYear(testDateTime)==expected_getYear)
    
def test_getMonth():
    expected_getMonth='06'
    assert(getMonth(testDateTime)==expected_getMonth)

def test_getDay():
    expected_getDay='09'
    assert(getDay(testDateTime)==expected_getDay)

def test_getHour():
    expected_getHour='02'
    assert(getHour(testDateTime)==expected_getHour)
    
def test_getMin():
    expected_getMin='18'
    assert(getMin(testDateTime)==expected_getMin)
    
def test_getSec():
    expected_getSec='29'
    assert(getSec(testDateTime)==expected_getSec)