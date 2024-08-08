import sys
sys.path.insert(0, './src/webpage')
print(sys.path)
import removeBorrowed 

def notime(booklist):
    booklist_notime = {}
    for borrower_id, books in booklist.items():
        booklist_notime[borrower_id] = [[book[0], book[1]] for book in books]
    return booklist_notime

def test_remove():
    egBooklist = {'test&1234567': [['Book 1', 'Location 1', '2024-06-15 21:28:26'], 
                                   ['Book 3', 'Location 1', '2024-06-15 21:28:30'], 
                                   ['Book 6', 'Location 2', '2024-06-15 21:28:33']],
                'test2&7654321': [['Book 5', 'Location 1', '2024-06-15 21:28:26'], 
                                  ['Book 3', 'Location 1', '2024-06-15 21:28:30'], 
                                  ['Book 6', 'Location 2', '2024-06-15 21:28:33']]}
    
    egBorrowlist = {'test&1234567': [['Book 3', '2024-06-15 21:30:29'], 
                                     ['Book 1', '2024-06-15 21:30:29']],
                    'test2&7654321': [['Book 5', '2024-06-15 21:28:26']]}
    
    booklist = removeBorrowed.remove(egBooklist, egBorrowlist)

    expected_booklist= {'test&1234567':[['Book 6', 'Location 2', '2024-06-15 21:28:33']],
                        'test2&7654321':[['Book 3', 'Location 1', '2024-06-15 21:28:30'], 
                                         ['Book 6', 'Location 2', '2024-06-15 21:28:33']]}
    
    booklist_notime = notime(booklist)
    expected_booklist_notime = notime(expected_booklist)

    assert booklist_notime == expected_booklist_notime