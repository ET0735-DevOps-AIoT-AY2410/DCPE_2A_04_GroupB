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
        fieldnames = ['username', 'password']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow({'username': username, 'password': password})