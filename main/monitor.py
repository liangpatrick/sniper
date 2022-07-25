import os
import datetime
import re
# installed
from flask import Flask, jsonify, request
import json
import requests
import threading
# own files
import dbMethods
import notify

# Create Flask object
app = Flask(__name__)

baseURL = "http://sis.rutgers.edu/soc/api/openSections.json?year="
# rest of the URL template: {year}&term={term}&campus=NB
courseURL = "https://sis.rutgers.edu/soc/api/courses.json?year="
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
# Endpoint that will only accept POST requests
@app.route("/addCode", methods=['POST'])
def updateDB():
  params = request.get_json()
  netid = params["netid"]
  codes = params["codes"]
  if not(codes.isnumeric()):
    return "Non valid entry"
  # ADD FILTER FOR INPUTS
  filtered = re.sub(r'[^a-zA-Z0-9]', '', netid)
  courseDict = getCourseInfo(getCourses())
  print(filtered)
  if str(code) not in courseDict:
    return "NON-VALID CODE, PLEASE TRY AGAIN"
  mycursor = db.cursor()
  mycursor.execute("ROLLBACK")
  dbMethods.addUser(db, filtered)
  dbMethods.addCode(db, code, filtered)
  # dbMethods.showCodes(db)
  # dbMethods.delCode(db, "05386")
  # dbMethods.showCodes(db)
  print("Success")
  return "Success"

def getCourseInfo(courses):

  map = {}

  # Going through the courses in the subject
  for course in courses:
  
    sections = course['sections']
    title = course['title']
    # going through the sections in the course
    for section in sections:
      index = section['index']
      map[index] = title      


  return map

# gets the courses
def getCourses():
  month = datetime.datetime.now().month
  print(month)
  year = datetime.datetime.now().year
  print(year)
  term = ""
  # determines season
  if month > 3 and month < 10:
    term = termKey["fall"]
  elif month > 10:
    term = termKey["spring"]
    ++year
  elif month < 4:
    term = termKey["spring"]
  elif month == 3:
    term = termKey["summer"]
  var = False
  finalURL = f'{courseURL}{year}&term={term}&campus=NB'
  print(finalURL)
  while not(var):
      try:
          res = requests.get(finalURL)
          var = True
          print("Connected")
      except:
          print("Failed to connect")
  return res.json()
# # temp
#   year = datetime.datetime.now().year
#   # print(year)
#   term = termKey["fall"]
#   finalURL = f'{courseURL}{year}&term={term}&campus=NB'


# updateDB("pzl4", "17471")
  
# setting up threads to monitor each separate term
def createThreads():
  count = 0
  while True:
    day = datetime.datetime.now().day
    # print(day)
    month = datetime.datetime.now().month
    # print(month)
    year = datetime.datetime.now().year
    # print(year)
    # only happens once a month and at 6 am
    hour = datetime.datetime.now().hour
    if day != 1 and hour == 6:
      count = 0
      continue
    if day == 1 and count == 0:
      count += 1
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
 

# def testThread():
#   year = datetime.datetime.now().year
#   # print(year)
#   # only happens once a month and at 6 am
#   term = termKey["fall"]
#   finalURL = f'{baseURL}{year}&term={term}&campus=NB'
#   print(finalURL)
#   fall = threading.Thread(target = monitorThread, args = ("9", 17, finalURL))
#   fall.start()

# will simply monitor when it is time to send a notification, in which it will alert another file to do so
def monitorThread(term, endMonth, URL):
  print(term + " thread has been opened")
  # infinite loop until the registration period ends
  while True:
    var = False
    
    # checks to see how long it will sleep until monitoring again
    hour = datetime.datetime.now().hour
    if hour < 6 or hour > 23:
      min = datetime.datetime.now().minute
      difference = 60 - crntMin
      converted = difference * 60000
      print("Hours is " + hour)
      print("Sleeping ... waiting " + difference + " minutes")
      sleep(converted)
    # attempt to connect to the endpoint
    while not(var):
      try:
          res = requests.get(URL)
          var = True
          # print("Connected")
      except:
          print("Failed to connect")

    # creates a json object which is effectively a dictionary in python
    openSections = res.json()
    
    mycursor.execute("SELECT * FROM Codes")
    course_codes = mycursor.fetchall()
    # iterates through each row in the TABLE Codes
    for row in course_codes:
      if str(row[2]) not in openSections:
        continue
      # sends the row tuple which is: (id, uid, codes)
      uid = row[1]
      mycursor.execute("SELECT netid FROM Users WHERE uid = %s", (uid,))
      netid = mycursor.fetchall()
      filtered = re.sub(r'[^a-zA-Z0-9]', '', str(netid[0]))
      id = row[0]
      codes = str(row[2])
      map = getCourseInfo(getCourses())
      courseName = map[codes]
      notify.push(id, filtered, courseName, codes)
      if(datetime.datetime.now().month == endMonth):
        break
  # will cause thread to end
  print(term + " thread has been closed")
  return

createThreads()
# count = 0
# if count is 0:
#   notify.push(1, "pzl4", "haha", 17471)
#   count += 1
# testThread()




      