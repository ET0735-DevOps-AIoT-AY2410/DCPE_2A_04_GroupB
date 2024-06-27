def getYear(dateTime):
    year = dateTime[:4]
    return year
    
def getMonth(dateTime):
    month = dateTime[5:7]
    return month

def getDay(dateTime):
    day = dateTime[8:10]
    return day
    
def getHour(dateTime):
    hours = dateTime[11:13]
    return hours
    
def getMin(dateTime):
    minutes = dateTime[14:16]
    return minutes
    
def getSec(dateTime):
    seconds = dateTime[17:19]
    return seconds

def main():
    testDateTime = '2024-06-09 02:18:29'
    print(getYear(testDateTime))
    print(getMonth(testDateTime))
    print(getDay(testDateTime))
    print(getHour(testDateTime))
    print(getMin(testDateTime))
    print(getSec(testDateTime))

if __name__ == '__main__':
    main()