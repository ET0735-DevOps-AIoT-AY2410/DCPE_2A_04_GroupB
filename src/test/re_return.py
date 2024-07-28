import time
from threading import Thread

# Mock classes for LCD and Keypad
class MockLCD:
    def __init__(self):
        self.display = ["", ""]

    def lcd_clear(self):
        self.display = ["", ""]

    def lcd_display_string(self, message, line):
        self.display[line-1] = message
        print(f"LCD Line {line}: {message}")

class MockKeypad:
    def __init__(self, key_press_callback):
        self.key_press_callback = key_press_callback

    def init(self, key_press_callback):
        self.key_press_callback = key_press_callback

    def get_key(self):
        # Simulate key press sequence
        keys = ['1', '2', '3', '4', '*']
        for key in keys:
            time.sleep(1)  # Simulate delay between key presses
            self.key_press_callback(key)

# Mock for parseBooklist.getReserve
def mock_getReserve(borrowList, person):
    info = person[0] + '&' + person[1]
    return borrowList.get(info, [])

def key_pressed(key):
    global returnIndex
    global password
    password = key
    print(password)
    returnIndex.append(password)

def displayBorrowed(borrowList, person, books):
    displayList = mock_getReserve(borrowList, person)
    if len(displayList) % 2 == 0:
        for i in range(len(displayList)):
            if i % 2 == 1:
                lcd.lcd_clear()
                lcd.lcd_display_string(books[displayList[i-1][0]] + ' press ' + str(i), 1)
                lcd.lcd_display_string(books[displayList[i][0]] + ' press ' + str(i+1), 2)
                time.sleep(0.5)
    elif len(displayList) % 2 == 1:
        for i in range(len(displayList)):
            if i % 2 == 1 and i < (len(displayList) - 1):
                lcd.lcd_clear()
                lcd.lcd_display_string(books[displayList[i-1][0]] + ' press ' + str(i), 1)
                lcd.lcd_display_string(books[displayList[i][0]] + ' press ' + str(i+1), 2)
                time.sleep(0.5)
            elif i == (len(displayList) - 1):
                lcd.lcd_clear()
                lcd.lcd_display_string(books[displayList[i][0]] + ' press ' + str(i+1), 1)
                time.sleep(0.5)

def returnBook(returnIndex, borrowList, person):
    returnIndex.remove('*')
    info = person[0] + '&' + person[1]
    reserveList = {}
    
    reserveList.setdefault(info, [])
    for index in returnIndex:
        index = int(index)  # Convert index to integer
        if index <= len(borrowList[info]) and index > 0:
            reserveList[info].append([borrowList[info][index-1][0]])

    return reserveList

def main():
    global password
    global returnIndex
    password = ''
    returnIndex = []

    # Use mock classes
    global lcd
    lcd = MockLCD()
    keypad = MockKeypad(key_pressed)

    keypad_thread = Thread(target=keypad.get_key)
    keypad_thread.start()

    egBorrowList = {'Test1&1234567': [['Book 1', '2024-06-15 21:30:29'], 
                                      ['Book 3', '2024-06-15 21:30:29'], 
                                      ['Book 2', '2024-06-15 21:30:29'], 
                                      ['Book 9', '2024-06-15 21:30:29'],
                                      ['Book 6', '2024-06-15 21:30:29']],
                    'Test2&7654321': [['Book 5', '2024-06-15 21:28:26']]}

    person = ['Test1', '1234567']
    
    books = {
        'Book 1': 'Introduction to Python',
        'Book 2': 'Advanced Python',
        'Book 3': 'Data Science with Python',
        'Book 9': 'Machine Learning with Python',
        'Book 6': 'Deep Learning with Python'
    }

    while password != '*':
        displayBorrowed(egBorrowList, person, books)
        time.sleep(1)
    
    print("Return Index:", returnIndex)
    returned_books = returnBook(returnIndex, egBorrowList, person)
    print("Returned Books:", returned_books)

if __name__ == '__main__':
    main()
