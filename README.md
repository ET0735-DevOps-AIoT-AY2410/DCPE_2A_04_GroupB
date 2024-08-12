# Library Book Reservation and Collection System

This contains all the documents denoting Software Requirements Specifications(SRS), and sprint planning

It also contains the code for the Library Book Reservation and Collection System

Before running app:
- IP of server updated in:
    - config .js files
    - libInterface.py

# Our functions
webpage.py: 
- Includes all the user interface functions, which the user would be able to login, search up and reserve books, and pay fines.

scanbarcode.py:
- captures images using the Raspberry Pi Camera and saves them to a specified file path.

barcode.py: 
- decodes barcodes and return as a value.

calcFine.py:
- calculates overdue books and fines.
- checks if any books are overdue.
- provides a fine amount for each borrower.

getFromRpi.py:
- interacts with a REST API to manage book reservations and fines.
- processes book reservation, updates system.

readWriteBooks.py:
- manages book data stored in a CSV file.
- loads book data, adds new books, removes books, and changes the status from borrowed to reserved.

removeReserved.py:
checks if reserved books have surpassed their reservation period and remove them from the list if they are overdue.
- scans through a dictionary of borrowed books.

update.py:
integrates various operations to keep your book management system up to date.
- loads the current reserve and borrow lists from the CSV file.
- calls checkReserveOver to remove any overdue reserved books.
- uses calcFine.fining to calculate fines based on overdue borrowed books.
- updates the user fines. 

userInfo.py:
- handles user account management and fine tracking in the library system.
- provides functions to load user passwords, create new user accounts, update user fines, and retrieve fine information.

collection.py:
- allows users to collect reserved books from a specified location.
- ensures users do not exceed the maximum borrowing limit of 10 books.
- provides feedback to the user on the status of their collection via an LCD display.
- simulates book dispensing using a motor.
- updates the user's borrow list after successful book collection.

dispense.py:
controls the hardware components of a book dispensing system. The system uses a servo motor, DC motor, LED, and an LCD display to simulate the process of dispensing a book. The script initializes the hardware, controls the dispensing mechanism, and provides real-time feedback via the LCD.
- the servo motor is used to open and close the dispensing mechanism.
- the DC motor drives the book dispensing mechanism.
- the LED provides a visual indication when the book is being dispensed.
- the LCD display provides real-time status updates to the user.

extendTime.py:
extends the loan period for borrowed books in a library system. The system interacts with a hardware keypad for user input, an LCD display for providing feedback, and supports loan extensions for individual books. The extension period is simulated as 7 minutes instead of the typical 7 days for demonstration purposes.
- users can enter their book selection via a keypad to extend the loan period.
- extends the loan period for selected books by 7 minutes.
- displays book details and extension status on an LCD.
- the script uses threading to handle keypad input concurrently with other operations.

getBooklist.py:
- retrieves a list of books that have been reserved by users.
- retrieves a list of outstanding fines for users.
- retrieves a list of registered users in the system.
- retrieves a dictionary of book titles or other relevant information.

lib_loc.py:
continuously displays the location based on the state of a slide switch. The location is displayed on an LCD screen, and the script uses threading to constantly update the display in real-time as the switch is toggled.
- the script reads the state of a slide switch to determine the current location.
- the determined location is displayed on an LCD screen.
- uses threading to continuously update the LCD display without blocking the main program.

libInterface.py:
integrates hardware components like an LCD display, keypad, DC motor, and RFID scanner with a Flask web server. It manages book reservations, returns, fine payments, and book extensions. The system authenticates users, interacts with a backend server to fetch real-time data, and allows users to perform various library operations through a user-friendly hardware interface.
- displays real-time instructions and feedback to the user.
- allows users to select options and enter data.
- automates physical interactions, such as book dispensing.
- handles communication with the backend and external modules.
- ensures smooth, non-blocking operation by handling multiple tasks simultaneously.

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