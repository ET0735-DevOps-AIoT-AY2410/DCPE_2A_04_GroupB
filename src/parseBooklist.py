def getNameList(bookList):
    name = bookList.keys()
    nameList = []
    for i in name:
        nameList.append(i.split('&'))
    return nameList

def findPerson(nameList, nameOrNum):
    for i in range(len(nameList)):
        if nameOrNum in nameList[i]:
            return True, nameList[i]
    return [False]

def getReserve(Booklist, person):
    
    info = person[0] + '&' + person[1]

    return Booklist[info]

def main():
    egBooklist = {'Test1&1234567': [['Book 1', 'Location 2', '2024-06-09 15:07:23'], 
                                    ['Book 2', 'Location 2', '2024-06-09 15:08:12']],
                  'Test2&7654321': [['Book 1', 'Location 1', '2024-06-09 15:34:32']]}
    name = 'Test1'
    
    nameList = getNameList(egBooklist)
    print(nameList)
    
    name = '7654321'
    person = findPerson(nameList, name)[1]

    print(getReserve(egBooklist, person))


if __name__ == '__main__':
    main()