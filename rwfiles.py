import csv
from auth import *

def readCSV(filename):
    # reading config csv file
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        data_rows = []
        # extracting field names through first row
        fields = next(csvreader)
    
        # extracting each data row one by one
        for row in csvreader:
            data_rows.append(row)

        return fields, data_rows

def viewRecord(username, data_rows, allowedFields):
    
    for row in data_rows:
        if (row[0]==username):
            for i in allowedFields:
                print(row[i], end=" ")
            else:
                print("")

def viewUsers(username, config_rows):
    
    for row in config_rows:
        if (row[0]==username):
            print(" ".join([field for field in row]))
            print("")

def writeRecord(filename, username, first, last, location, contact, sickness, drug, lab):
    
    with open(filename, 'a') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        
        # writing the data rows
        csvwriter.writerow([username, first, last, location, contact, sickness, drug, lab])

def createUser(filename, username,password,usertype,privilege):
    hash = hashlib.md5(password.encode())
    with open(filename, 'a') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        
        # writing the config rows
        csvwriter.writerow([username,hash.hexdigest(),usertype,privilege])