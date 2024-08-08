# Library Book Reservation and Collection System

This contains all the documents denoting Software Requirements Specifications(SRS), and sprint planning

It also contains the code for the Library Book Reservation and Collection System

Before running app:
- IP of server updated in:
    - static .js files
    - libInterface.py
- IP of RPi updated in:
    - webpage.py

# Our functions
webpage.py: 
- Includes all the user interface functions, which the user would be able to login, search up and reserve books, and pay fines

barcode.py: 
- Able to scan barcodes and return as a value

collection.py:
- Allows users to collect reserved books from a specified location.
- Ensures users do not exceed the maximum borrowing limit of 10 books.
- Provides feedback to the user on the status of their collection via an LCD display.
- Simulates book dispensing using a motor.
- Updates the user's borrow list after successful book collection.

dispense.py:
controls the hardware components of a book dispensing system. The system uses a servo motor, DC motor, LED, and an LCD display to simulate the process of dispensing a book. The script initializes the hardware, controls the dispensing mechanism, and provides real-time feedback via the LCD.
- The servo motor is used to open and close the dispensing mechanism.
- The DC motor drives the book dispensing mechanism.
- The LED provides a visual indication when the book is being dispensed.
- The LCD display provides real-time status updates to the user.

extendTime.py:
extends the loan period for borrowed books in a library system. The system interacts with a hardware keypad for user input, an LCD display for providing feedback, and supports loan extensions for individual books. The extension period is simulated as 7 minutes instead of the typical 7 days for demonstration purposes.
- Users can enter their book selection via a keypad to extend the loan period.
- Extends the loan period for selected books by 7 minutes.
- Displays book details and extension status on an LCD.
- The script uses threading to handle keypad input concurrently with other operations.

getBooklist.py:
- Retrieves a list of books that have been reserved by users.
- Retrieves a list of outstanding fines for users.
- Retrieves a list of registered users in the system.
- Retrieves a dictionary of book titles or other relevant information.

lib_loc.py:
continuously displays the location based on the state of a slide switch. The location is displayed on an LCD screen, and the script uses threading to constantly update the display in real-time as the switch is toggled.
- The script reads the state of a slide switch to determine the current location.
- The determined location is displayed on an LCD screen.
- Uses threading to continuously update the LCD display without blocking the main program.

libInterface.py:
integrates hardware components like an LCD display, keypad, DC motor, and RFID scanner with a Flask web server. It manages book reservations, returns, fine payments, and book extensions. The system authenticates users, interacts with a backend server to fetch real-time data, and allows users to perform various library operations through a user-friendly hardware interface.
- Displays real-time instructions and feedback to the user.
- Allows users to select options and enter data.
- Automates physical interactions, such as book dispensing.
- Handles communication with the backend and external modules.
- Ensures smooth, non-blocking operation by handling multiple tasks simultaneously.

parseBooklist.py:
- Extracts names and IDs from a dictionary and splits them.
- Searches for a person by name or ID and returns their details.
- Retrieves reservation information for a specific person.

parseDateTime.py:
- extracts specific components from a date-time string in the format yyyy-mm-ss hh:mm:ss

removeBorrowed.py:
- manages and updates a book list by removing borrowed books based on a provided borrowing list. 
- updates the book list by removing entries that are present in the borrow list.

returnBook.py:
- manages the return of borrowed books
- uses a keypad for user input and an LCD display to interact with the user.
- allows users to view borrowed books, select which ones to return
- pdates the book list accordingly.

scanRFID.py:
- handles the scanning of RFID cards using an RFID reader
- displays messages on an LCD screen
- scans RFID cards for various purposes, such as paying fines etc..

To run container:
```
docker run -it --privileged=true \
-p 5001:5001 \
--mount type=bind,source="$(sudo find /home/pi -name scannedImage)",target=/app/scannedImage \
dionchoy/testlib
```