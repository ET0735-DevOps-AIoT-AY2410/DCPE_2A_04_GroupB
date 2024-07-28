import pytest
from re_dispense import dispenseBook, MockLCD, MockServo, MockDCMotor

def test_dispenseBook():
    lcd = MockLCD()
    servo = MockServo()
    dc_motor = MockDCMotor()

    dispenseBook(lcd, servo, dc_motor)

    assert lcd.commands == [
        "LCD cleared",
        "LCD Line 1: Valid Card",
        "LCD Line 2: Dispensing..."
    ]
    assert servo.positions == [
        "Servo set to position 0",
        "Servo set to position 90",
        "Servo set to position 0"
    ]
    assert dc_motor.speeds == [
        "DC Motor set to speed 100",
        "DC Motor set to speed 0"
    ]

if __name__ == '__main__':
    pytest.main()
