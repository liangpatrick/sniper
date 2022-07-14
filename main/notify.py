import os
import datetime
# installed

import requests
# own files
import dbMethods

baseURL = "http://sims.rutgers.edu/webreg/editSchedule.htm?login=cas&semesterSelection="
# 92021&indexList=14006
db = dbMethods.connect()
mycursor = db.cursor()

termKey= {
    'summer': 7,
    'winter': 0,
    'fall': 9,
    'spring': 1 
}

def getTerm():
    month = datetime.datetime.now().month
    print(month)
    term = ""
    if month > 3 and month < 10:
        term = termKey["fall"]
    elif month > 10:
        term = termKey["spring"]
    elif month < 4:
        term = termKey["spring"]
    elif month == 3:
        term = termKey["summer"]

    return term

def push(row):
    # sends message
    year = datetime.datetime.now().year
    print(year)
    try:
        finalURL = f'{baseURL}{getTerm()}{year}&indexList={row[2]}'
        print(finalURL)
        dbMethods.delCode(db, row[2])
    except Exception as err:
        print("Exception raised:", err)

push((1, 1, "05386"))