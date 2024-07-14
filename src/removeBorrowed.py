def remove(bookList, borrowList):
    for info in borrowList:
        if info in bookList:
            for book in borrowList[info]:
                for compareBook in bookList[info]:
                    if book[0] in compareBook:
                        bookList[info].remove(compareBook)

    return bookList

def main():
    egBooklist = {'test&1234567': [['Book 1', 'Location 1', '2024-06-15 21:28:26'], 
                                   ['Book 3', 'Location 1', '2024-06-15 21:28:30'], 
                                   ['Book 6', 'Location 2', '2024-06-15 21:28:33']],
                'test2&7654321': [['Book 5', 'Location 1', '2024-06-15 21:28:26'], 
                                  ['Book 3', 'Location 1', '2024-06-15 21:28:30'], 
                                  ['Book 6', 'Location 2', '2024-06-15 21:28:33']]}
    
    egBorrowlist = {'test&1234567': [['Book 3', '2024-06-15 21:30:29'], 
                                     ['Book 1', '2024-06-15 21:30:29']],
                    'test2&7654321': [['Book 5', '2024-06-15 21:28:26']]}
    
    print(remove(egBooklist, egBorrowlist))


if __name__ == '__main__':
    main()