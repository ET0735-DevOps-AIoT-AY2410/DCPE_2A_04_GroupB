import sys
sys.path.insert(0, './src/webpage')
print(sys.path)
from datetime import datetime, timedelta
from calcFine import check_overdue_books, fining

def test_overdue_books():
    current_date = datetime.now() 

    borrowed_books = {
        'Test1&1234567': [['Book 1', (current_date - timedelta(minutes=20)).strftime('%Y-%m-%d %H:%M:%S')],
                          ['Book 2', (current_date - timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S')],
                          ['Book 3', (current_date - timedelta(minutes=30)).strftime('%Y-%m-%d %H:%M:%S')]],
        'Test2&7654321': [['Book 1', (current_date - timedelta(minutes=25)).strftime('%Y-%m-%d %H:%M:%S')]]
    }

    overdue_books = check_overdue_books(borrowed_books)

    expected_overdue_books = [
        ('Book 1', datetime.strptime((current_date - timedelta(minutes=20)).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'), 'Test1&1234567'),
        #('Book 2', datetime.strptime((current_date - timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'), 'Test1&1234567'),
        ('Book 3', datetime.strptime((current_date - timedelta(minutes=30)).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'), 'Test1&1234567'),
        ('Book 1', datetime.strptime((current_date - timedelta(minutes=25)).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'), 'Test2&7654321')
    ]

    # Check if the number is correct
    assert len(overdue_books) == len(expected_overdue_books)
    for overdue_book, expected in zip(overdue_books, expected_overdue_books):
        assert overdue_book[0] == expected[0]
        assert overdue_book[1] == expected[1]
        assert overdue_book[2] == expected[2]

def test_fining():
    current_date = datetime.now()
    borrowed_books = {
        'Test1&1234567': [['Book 1', (current_date - timedelta(minutes=20)).strftime('%Y-%m-%d %H:%M:%S')],
                          ['Book 2', (current_date - timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S')],
                          ['Book 3', (current_date - timedelta(minutes=30)).strftime('%Y-%m-%d %H:%M:%S')]],
        'Test2&7654321': [['Book 1', (current_date - timedelta(minutes=25)).strftime('%Y-%m-%d %H:%M:%S')]]
    }

    fines = fining(borrowed_books)

    expected_fines = {
        'Test1&1234567': (0.15 * 2)+ (0.15 * 12),
        'Test2&7654321': (0.15 * 7)
    }

    # Check if the fines are calculated correctly
    assert fines == expected_fines

