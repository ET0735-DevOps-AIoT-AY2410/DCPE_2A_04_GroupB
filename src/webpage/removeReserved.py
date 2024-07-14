from datetime import datetime, timedelta
import readWriteBooks

def checkReserveOver(borrowed_books):
    current_date = datetime.now()

    for borrower_id, books in borrowed_books.items():
        for eachBook in books:
            name, location, date = eachBook
                
            borrow_date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            return_date = borrow_date + timedelta(minutes=5)  
            if current_date > return_date:
                readWriteBooks.removeBook(borrower_id, name)

def main():
    egBooklist = {'test&1234567': [['Book 1', 'Location 2', '2024-06-09 15:07:23'], 
                                    ['Book 2', 'Location 2', '2024-06-09 15:08:12']],
                  'Test2&7654321': [['Book 1', 'Location 1', '2024-06-09 15:34:32']]}
    
    checkReserveOver(egBooklist)
if __name__ == '__main__':
    main()