import os
import datetime
# installed
import json
import requests
from threading import Thread, Lock
# own files
import dbMethods
import notify

baseURL = "http://sis.rutgers.edu/soc/api/openSections.json?year="
# rest of the URL template: {year}&term={term}&campus=NB

# connect to sql database
db = dbMethods.connect()
mycursor = db.cursor()

# key bindings for terms
termKey= {
  'summer': 7,
  'winter': 0,
  'fall': 9,
  'spring': 1 
}

# updates sql DB and front end will always push the netid
def updateDB(netid, code):
  # ADD FILTER FOR INPUTS

  dbMethods.addUser(db, netid)
  dbMethods.addCode(db, code, netid)
  print("DONE")


# setting up threads to monitor each separate term
def createThreads():
  day = datetime.datetime.now().day
  month = datetime.datetime.now().month
  year = datetime.datetime.now().year
  # checks the first of every month if a thread should be created
  while True:
    if day == 1:
      if month == 3:
        term = termKey["summer"]
        finalURL = f'{baseURL}{year}&term={term}&campus=NB'
        print(finalURL)
        summer = threading.Thread(target = monitorThread, args = ("7", 9, finalURL))
        summer.start()
      if month == 10:
        term = termKey["winter"]
        finalURL = f'{baseURL}{year}&term={term}&campus=NB'
        print(finalURL)
        winter = threading.Thread(target = monitorThread, args = ("0", 1, finalURL))
        winter.start()
      if month == 4:
        term = termKey["fall"]
        finalURL = f'{baseURL}{year}&term={term}&campus=NB'
        print(finalURL)
        fall = threading.Thread(target = monitorThread, args = ("9", 10, finalURL))
        fall.start()
      if month == 11:
        term = termKey["spring"]
        finalURL = f'{baseURL}{year+1}&term={term}&campus=NB'
        print(finalURL)
        spring = threading.Thread(target = monitorThread, args = ("9", 10, finalURL))
        spring.start()
 

# will simply monitor when it is time to send a notification, in which it will alert another file to do so
def monitorThread(term, endMonth, URL):
  var = False
  # attempt to connect to the endpoint
  while not(var):
    i
    try:
        res = requests.get(URL)
        var = True
        print("Connected")
    except:
        print("Failed to connect")

  # creates a json object which is effectively a dictionary in python
  openSections = res.json()

  while True:
    mycursor.execute("SELECT * FROM Codes")
    course_codes = mycursor.fetchall()
    # iterates through each row in the TABLE Codes
    for row in course_codes:
      if row[2] not in openSections:
        continue
      # sends the row tuple which is: (id, uid, codes)
      notify.push(row)

    



      
  
# dbMethods.showCodes(db)
