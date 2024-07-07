import csv
import os

def loadBooks():
    bookList = {}
    file_path = os.path.join(os.path.dirname(__file__), 'reserveList.csv')
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['id'] not in bookList:
                bookList[row['id']] = [[row['books'], row['location'], row['date']]]
            else:
                bookList[row['id']].append([row['books'], row['location'], row['date']])
    return bookList

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
    print(tempList)

    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['id', 'books', 'location', 'date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in tempList:
            writer.writerow(row)

def main():
    id = 'test2&7654321'
    book = 'Book 1'
    location = 'Location 2'
    date = '2024-07-07 20:59:56'
    '''print(loadBooks())
    addBook(id, book, location, date)'''
    removeBook(id, book)

if __name__ == '__main__':
    main()