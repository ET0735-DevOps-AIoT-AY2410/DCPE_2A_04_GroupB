import csv
import os

def loadBooks():
    reserveList = {}
    borrowList = {}
    file_path = os.path.join(os.path.dirname(__file__), 'reserveList.csv')
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['location'] != 'borrowed':
                if row['id'] not in reserveList:
                    reserveList[row['id']] = [[row['books'], row['location'], row['date']]]
                else:
                    reserveList[row['id']].append([row['books'], row['location'], row['date']])

            else:
                if row['id'] not in borrowList:
                    borrowList[row['id']] = [[row['books'], row['date']]]
                else:
                    borrowList[row['id']].append([row['books'], row['date']])
    return reserveList, borrowList

def addBook(id, book, location, date):
    file_path = os.path.join(os.path.dirname(__file__), 'reserveList.csv')
    with open(file_path, 'a', newline='') as csvfile:
        fieldnames = ['id', 'books', 'location', 'date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow({'id': id, 'books': book, 'location': location, 'date': date})

def removeBook(id, book):
    tempList = []
    file_path = os.path.join(os.path.dirname(__file__), 'reserveList.csv')
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if not (row['id'] == id and row['books'] == book):
                tempList.append(row)

    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['id', 'books', 'location', 'date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in tempList:
            writer.writerow(row)

def changeToReserve(borrowList):
    for id in borrowList:
        for book in borrowList[id]:
            removeBook(id, book[0])
            addBook(id, book[0], 'borrowed', book[1])

def main():
    id = 'test2&7654321'
    book = 'Book 1'
    location = 'Location 2'
    date = '2024-07-07 20:59:56'
    '''print(loadBooks())
    addBook(id, book, location, date, 0)'''
    removeBook(id, book)

    print(loadBooks())

    borrowed_books = {'test&1234567': [['Book 1', '2024-07-08 16:21:23'], 
                                       ['Book 3', '2024-07-08 16:30:12']]}
    
    changeToReserve(borrowed_books)
    
    print(loadBooks())

if __name__ == '__main__':
    main()