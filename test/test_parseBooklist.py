from parseBooklist import getNameList, findPerson, getReserve

egBooklist = {'Test1&1234567': [['Book 1', 'Location 2', '2024-06-09 15:07:23'], 
                                ['Book 2', 'Location 2', '2024-06-09 15:08:12']],
              'Test2&7654321': [['Book 1', 'Location 1', '2024-06-09 15:34:32']]}


def test_getNameList():

    expected_nameList = [['Test1', '1234567'], ['Test2', '7654321']]
    assert (getNameList(egBooklist) == expected_nameList)

def test_findPerson():
    nameList = [['Test1', '1234567'], ['Test2', '7654321']]
    
    nameOrNum = '1234567'
    expected_result = (True, ['Test1', '1234567'])
    assert findPerson(nameList, nameOrNum) == expected_result

    nameOrNum = 'Test2'
    expected_result = (True, ['Test2', '7654321'])
    assert findPerson(nameList, nameOrNum) == expected_result

    nameOrNum = '2024069'
    expected_result = [False]
    assert findPerson(nameList, nameOrNum) == expected_result

def test_getReserve():
   
    person = ['Test1', '1234567']
    expected_result = [['Book 1', 'Location 2', '2024-06-09 15:07:23'], 
                       ['Book 2', 'Location 2', '2024-06-09 15:08:12']]
    assert getReserve(egBooklist, person) == expected_result

    person = ['Test2', '7654321']
    expected_result = [['Book 1', 'Location 1', '2024-06-09 15:34:32']]
    assert getReserve(egBooklist, person) == expected_result

  