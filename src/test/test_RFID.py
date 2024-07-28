import pytest
from re_RFID import scan, MockLCD, MockRFIDReader

def test_scan():
    lcd = MockLCD()
    reader = MockRFIDReader()

    id = scan(lcd, reader)

    assert id == "12345678"
    assert lcd.commands == [
        "LCD cleared",
        "LCD Line 1: Scan your card",
        "LCD Line 2: to pay fine"
    ]

if __name__ == '__main__':
    pytest.main()
