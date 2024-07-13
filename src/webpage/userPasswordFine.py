import os
import csv

def load_passwords():
    passwords = {}
    file_path = os.path.join(os.path.dirname(__file__), 'passwords.csv')
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            passwords[row['username']] = row['password']
    return passwords

def createAcc(username, password):
    passwords = load_passwords()
    file_path = os.path.join(os.path.dirname(__file__), 'passwords.csv')
    with open(file_path, 'a', newline='') as csvfile:
        fieldnames = ['username', 'password', 'fine']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow({'username': username, 'password': password, 'fine': 0})

def addFine(fineList):
    tempList = []
    file_path = os.path.join(os.path.dirname(__file__), 'passwords.csv')
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['username'] in fineList:
                row['fine'] = fineList[row['username']]
            print(row)
            tempList.append(row)

    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['username', 'password', 'fine']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in tempList:
            writer.writerow(row)

def loadFine():
    fines = {}
    file_path = os.path.join(os.path.dirname(__file__), 'passwords.csv')
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if float(row['fine']) > 0:
                fines[row['username']] = float(row['fine'])
    return fines