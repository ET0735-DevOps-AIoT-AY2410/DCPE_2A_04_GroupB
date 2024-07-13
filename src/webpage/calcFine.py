from datetime import datetime, timedelta

def check_overdue_books(borrowed_books):
    current_date = datetime.now()
    overdue_books=[] 

    for borrower_id, book_name in borrowed_books.items():
        for book in book_name:
            book_name, borrow_date_str = book

            if borrow_date_str[-1:] == 'E':
                borrow_date_str = borrow_date_str[:-1]
                
            borrow_date = datetime.strptime(borrow_date_str, '%Y-%m-%d %H:%M:%S')
            return_date = borrow_date + timedelta(minutes=18)  
            if current_date > return_date:
                overdue_books.append((book_name, borrow_date, borrower_id))
    
    return overdue_books

def fining(borrowed_books):
    overdue_books = check_overdue_books(borrowed_books)
    user_fine = {}  # to store fines for each user
    
    for book_name, borrow_date, borrower_id in overdue_books:
        overdue_seconds = (datetime.now() - (borrow_date + timedelta(minutes=18))).total_seconds()
        overdue_minutes = round(overdue_seconds / 60)  # round to the nearest minute
        fine = 0.15 * overdue_minutes
        if borrower_id in user_fine:
            user_fine[borrower_id] += fine
        else:
            user_fine[borrower_id] = fine

    return user_fine

def main():
    borrowed_books= {'Test1&1234567': [['Book 1', '2024-07-03 14:30:23E'], 
                                       ['Book 2', '2024-07-03 14:30:12'], 
                                       ['Book 3', '2024-07-03 14:30:12']],
                     'Test2&7654321': [['Book 1', '2024-07-03 14:30:32']]}

    fineList = fining(borrowed_books)
    print(fineList)
    
    for borrower_id, fine in fineList.items():
        print(f"Dear user {borrower_id}, please pay your fine fee of ${fine:.2f} for the overdue books.")

if __name__ == '__main__':
    main()