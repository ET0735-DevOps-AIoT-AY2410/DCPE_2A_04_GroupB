import time
from unittest.mock import patch, call
import pytest

# Assuming the script file is named re_collection.py and it's located in src directory
from re_collection import collectBook, combineList

# Mock implementation of the LCD display
class MockLCD:
    def lcd_display_string(self, message, line):
        print(f"LCD Line {line}: {message}")

# Mock implementation of the dispense module
class MockDispense:
    @staticmethod
    def dispenseBook():
        print("Book dispensed")

lcd = MockLCD()

@pytest.fixture
def mock_lcd_display():
    with patch('re_collection.MockLCD.lcd_display_string', side_effect=lambda message, line: MockLCD().lcd_display_string(message, line)) as mock:
        yield mock

@pytest.fixture
def mock_dispense_book():
    with patch('re_collection.MockDispense.dispenseBook', side_effect=MockDispense.dispenseBook) as mock:
        yield mock

def test_collectBook(mock_lcd_display, mock_dispense_book):
    egBooklist = {
        'Test1&1234567': [['Book 1', 'Location 2', '2024-06-09 15:07:23'],
                          ['Book 2', 'Location 2', '2024-06-09 15:08:12']],
        'Test2&7654321': [['Book 1', 'Location 1', '2024-06-09 15:34:32']]
    }
    person = ['Test1', '1234567']
    location = 2

    borrowList = collectBook(person, location, egBooklist, 0)

    assert 'Test1&1234567' in borrowList
    assert len(borrowList['Test1&1234567']) == 2
    assert mock_dispense_book.call_count == 2
    
    # Ensure that the "Wrong Location" message was not called
    assert call("Wrong Location", 1) not in mock_lcd_display.call_args_list


@patch('re_collection.MockDispense.dispenseBook', side_effect=MockDispense.dispenseBook)
@patch('re_collection.MockLCD.lcd_display_string', side_effect=lambda message, line: MockLCD.lcd_display_string(MockLCD(), message, line))
def test_collectBook_wrong_location(mock_lcd_display, mock_dispense_book):
    egBooklist = {
        'Test1&1234567': [['Book 1', 'Location 1', '2024-06-09 15:07:23'],
                          ['Book 2', 'Location 1', '2024-06-09 15:08:12']],
        'Test2&7654321': [['Book 1', 'Location 2', '2024-06-09 15:34:32']]
    }
    person = ['Test1', '1234567']
    location = 2

    borrowList = collectBook(person, location, egBooklist, 0)

    assert 'Test1&1234567' in borrowList
    assert len(borrowList['Test1&1234567']) == 0
    mock_dispense_book.assert_not_called()
    mock_lcd_display.assert_any_call("Wrong Location", 1)

def test_combineList():
    borrowList = {
        'Test1&1234567': [['Book 3', '2024-06-15 21:30:29']],
        'Test2&7654321': [['Book 5', '2024-06-15 21:28:26']]
    }
    tempList = {
        'Test1&1234567': [['Book 1', '2024-06-09 15:07:23'],
                          ['Book 2', '2024-06-09 15:08:12']],
        'Test2&7654321': [['Book 6', '2024-06-09 15:34:32']]
    }

    combinedList = combineList(borrowList, tempList)

    assert len(combinedList['Test1&1234567']) == 3
    assert len(combinedList['Test2&7654321']) == 2

if __name__ == "__main__":
    pytest.main()
