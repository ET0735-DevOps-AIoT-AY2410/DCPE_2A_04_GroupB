import time

# Define the interfaces
class LCDInterface:
    def lcd_clear(self):
        pass

    def lcd_display_string(self, message, line):
        pass

class RFIDReaderInterface:
    def read_id_no_block(self):
        pass

# Mock classes for testing
class MockLCD(LCDInterface):
    def __init__(self):
        self.commands = []

    def lcd_clear(self):
        self.commands.append("LCD cleared")

    def lcd_display_string(self, message, line):
        self.commands.append(f"LCD Line {line}: {message}")

class MockRFIDReader(RFIDReaderInterface):
    def read_id_no_block(self):
        return 12345678

# Function that uses the interfaces
def scan(lcd: LCDInterface, reader: RFIDReaderInterface):
    lcd.lcd_clear()
    lcd.lcd_display_string("Scan your card", 1)
    lcd.lcd_display_string("to pay fine", 2)
    time.sleep(1)

    id = reader.read_id_no_block()
    id = str(id)

    return id

# Main function for actual execution
def main():
    # Using mock objects for demonstration and testing purposes
    lcd = MockLCD()
    reader = MockRFIDReader()
    print(scan(lcd, reader))

if __name__ == '__main__':
    main()
