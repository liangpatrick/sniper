import os
# installed
import requests
# own files
import dbMethods


db = dbMethods.connect()
mycursor = db.cursor()

def push(row):
    # sends message
    try:
        print("hello")
        dbMethods.delCode(db, row[2])
    except Exception as err:
        print("Exception raised:", err)