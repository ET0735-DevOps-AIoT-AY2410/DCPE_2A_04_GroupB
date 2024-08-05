import dispense
import time
from hal import hal_dc_motor as dc_motor
from hal import hal_lcd as LCD

lcd = LCD.lcd()

def collectBook(person, location, reserveList, noOfBorrowed):
    borrowList = {}
    info = person[0] + '&' + person[1]
    tempReserveList = reserveList[info]
    flag = 0
    
    borrowList.setdefault(info, [])
    for i in range(len(tempReserveList)):
        if tempReserveList[i][1] == ('Location ' + str(location)):
            tempReserveList[i].pop(1)
            tempReserveList[i][1] = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

            if len(borrowList[info]) + noOfBorrowed < 10:
                borrowList[info].append(tempReserveList[i])
            
            elif len(borrowList[info]) + noOfBorrowed >= 10:
                flag = 1
    
    if len(tempReserveList) != 0:
        if len(borrowList[info]) != 0:
            for i in range(len(borrowList[info])):
                dispense.dispenseBook()

            if flag == 1:
                lcd.lcd_display_string("Maximum books", 1)
                lcd.lcd_display_string("reached (10)", 2)
        
        lcd.lcd_display_string(f"{len(tempReserveList) - len(borrowList[info])} remaining books", 1)
        lcd.lcd_display_string(f"at Location {(location%2+1)}", 2)
        time.sleep(0.5)

    
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
    egReservelist = {'Test1&1234567': [['Book 1', 'Location 2', '2024-06-09 15:07:23'], 
                                   ['Book 2', 'Location 2', '2024-06-09 15:08:12']],
                  'Test2&7654321': [['Book 1', 'Location 1', '2024-06-09 15:34:32']]}
    person = ['Test1', '1234567']
    location = 2
    
    egBorrowlist = {'Test1&1234567': [['Book 3', '2024-06-15 21:30:29']],
                    'Test2&7654321': [['Book 5', '2024-06-15 21:28:26']]}

    dc_motor.init()
    tempList = collectBook(person, location, egReservelist, 0)
    print(tempList)

    print(combineList(tempList, egBorrowlist))

if __name__ == "__main__":
    main()
