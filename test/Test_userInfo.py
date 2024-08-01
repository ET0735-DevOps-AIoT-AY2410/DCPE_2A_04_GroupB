import sys
sys.path.insert(0, './src/webpage')
print(sys.path)
import userInfo

def test_load_passwords():
    result = userInfo.load_passwords()

    expectedResult = {'test&1234567':'pass1'}

    assert(result == expectedResult) 

def test_loadFine():
    expectedResult = {}
    result = userInfo.loadFine()
    assert(result == expectedResult)

def test_addFine():
    expectedResult = {'test&1234567':1.5}
    userInfo.addFine({'test&1234567':1.5})
    result = userInfo.loadFine()
    assert(result == expectedResult)
    userInfo.addFine({'test&1234567':0})