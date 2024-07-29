import time

# Mock implementation of the LCD display
class MockLCD:
    def lcd_display_string(self, message, line):
        print(f"LCD Line {line}: {message}")

# Mock implementation of the dispense module
class MockDispense:
    @staticmethod
    def dispenseBook():
        print("Book dispensed")

# Replace the hardware modules with mocks
lcd = MockLCD()

def collectBook(person, location, bookList, noOfBorrowed):
    borrowList = {}
    info = person[0] + '&' + person[1]
    tempBookList = bookList.get(info, [])
    flag = 0
    
    borrowList.setdefault(info, [])
    for i in range(len(tempBookList)):
        if tempBookList[i][1] == ('Location ' + str(location)):
            tempBookList[i].pop(1)
            tempBookList[i][1] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            if len(borrowList[info]) + noOfBorrowed < 10:
                borrowList[info].append(tempBookList[i])
            else:
                flag = 1
    
    if tempBookList:
        if not borrowList[info] and not flag:
            if location == 1:
                output = "Go to Location 2"
            elif location == 2:
                output = "Go to Location 1"
            lcd.lcd_display_string("Wrong Location", 1)
            lcd.lcd_display_string(output, 2)
            time.sleep(0.5)
        else:
            for i in range(len(borrowList[info])):
                MockDispense.dispenseBook()

            if flag == 1:
                lcd.lcd_display_string("Maximum books", 1)
                lcd.lcd_display_string("reached (10)", 2)
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
    egBooklist = {
        'Test1&1234567': [['Book 1', 'Location 2', '2024-06-09 15:07:23'], 
                          ['Book 2', 'Location 2', '2024-06-09 15:08:12']],
        'Test2&7654321': [['Book 1', 'Location 1', '2024-06-09 15:34:32']]
    }
    person = ['Test1', '1234567']
    location = 2
    
    egBorrowlist = {
        'Test1&1234567': [['Book 3', '2024-06-15 21:30:29']],
        'Test2&7654321': [['Book 5', '2024-06-15 21:28:26']]
    }

    tempList = collectBook(person, location, egBooklist, 0)
    print(tempList)

    print(combineList(tempList, egBorrowlist))

if __name__ == "__main__":
    main()
