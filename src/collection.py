import dispense
import time
from hal import hal_dc_motor as dc_motor
from hal import hal_lcd as LCD

lcd = LCD.lcd()

def collectBook(person, location, bookList):
    borrowList = {}
    info = person[0] + '&' + person[1]
    tempBookList = bookList[info]
    
    borrowList.setdefault(info, [])
    for i in range(len(tempBookList)):
        if tempBookList[i][1] == ('Location ' + str(location)):
            tempBookList[i].pop(1)
            tempBookList[i][1] = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

            if len(borrowList[info]) < 10:
                borrowList[info].append(tempBookList[i])
    
    if len(tempBookList) != 0:
        if len(borrowList[info]) == 0: 
            if location == 1:
                output = "Go to Location 2"
            elif location == 2:
                output = "Go to Location 1"
            lcd.lcd_display_string("Wrong Location", 1)
            lcd.lcd_display_string(output, 2)
            time.sleep(0.5)

        else:
            for i in range(len(borrowList[info])):
                dispense.dispenseBook()
    
    else:
        lcd.lcd_display_string("No reservations", 1)
        time.sleep(0.5)

    return borrowList

def combineList(borrowList, tempList):
    for info in tempList:
        if info in borrowList:
            for book in tempList[info]:
                borrowList[info].append(book)
            
        else:
            borrowList[info] = tempList[info]

    return borrowList

def main():
    egBooklist = {'Test1&1234567': [['Book 1', 'Location 2', '2024-06-09 15:07:23'], 
                                   ['Book 2', 'Location 2', '2024-06-09 15:08:12']],
                  'Test2&7654321': [['Book 1', 'Location 1', '2024-06-09 15:34:32']]}
    person = ['Test1', '1234567']
    location = 2
    
    egBorrowlist = {'Test1&1234567': [['Book 3', '2024-06-15 21:30:29']],
                    'Test2&7654321': [['Book 5', '2024-06-15 21:28:26']]}

    dc_motor.init()
    tempList = collectBook(person, location, egBooklist)
    print(tempList)

    print(combineList(tempList, egBorrowlist))

if __name__ == "__main__":
    main()
