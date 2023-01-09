import os
import datetime
import re
# installed
from flask import Flask, jsonify, request, Response
import json
import requests
import gevent
# own files
import dbMethods
import notify
import snipeAPI

app = Flask(__name__)


baseURL = "http://sis.rutgers.edu/soc/api/openSections.json?year="

# key bindings for terms
termKey= {
    'summer': 7,
    'winter': 0,
    'fall': 9,
    'spring': 1 
}
courseURL = "https://sis.rutgers.edu/soc/api/courses.json?year="
# rest of the URL template: {year}&term={term}&campus=NB
# connect to sql database
db = dbMethods.connect()
mycursor = db.cursor()

# setup multiple streams because can't use threads to do it






@app.route("/fall", methods=['GET'])
def fstream():
  def fall():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    term = "9"
    URL = finalURL = f'{baseURL}{year}&term={term}&campus=NB'
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
        netid = mycursor.fetchone()
        id = row[0]
        codes = str(row[2])
        map = getCourseInfo(getCourses(term))
        courseName = map[codes]
        yield f'SnipeRU: {netid[0]}! {courseName}({codes}) opened!\n\n'
        notify.push(id, netid[0], courseName, codes)
        dbMethods.delCode(db, codes)
      yield 'Nothing open\n\n'
      # if(datetime.datetime.now().month == endMonth):
      #   break
    # will cause thread to end
    print(term + " thread has been closed")
    return
  return Response(fall(), mimetype='text/event-stream')

@app.route("/winter", methods=['GET'])
def wstream():
  def winter():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    term = "0"
    URL = finalURL = f'{baseURL}{year}&term={term}&campus=NB'
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
        netid = mycursor.fetchone()
        id = row[0]
        codes = str(row[2])
        map = getCourseInfo(getCourses(term))
        courseName = map[codes]
        yield f'SnipeRU: {netid[0]}! {courseName}({codes}) opened!\n\n'
        notify.push(id, netid[0], courseName, codes)
        dbMethods.delCode(db, codes)
      yield 'Nothing open\n\n'
      # if(datetime.datetime.now().month == endMonth):
      #   break
    # will cause thread to end
    print(term + " thread has been closed")
    return
  return Response(winter(), mimetype='text/event-stream')

    
@app.route("/summer", methods=['GET'])
def sthread():
  def summer():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    term = "7"
    URL = finalURL = f'{baseURL}{year}&term={term}&campus=NB'
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
        netid = mycursor.fetchone()
        id = row[0]
        codes = str(row[2])
        map = getCourseInfo(getCourses(term))
        courseName = map[codes]
        yield f'SnipeRU: {netid[0]}! {courseName}({codes}) opened!\n\n'
        notify.push(id, netid[0], courseName, codes)
        dbMethods.delCode(db, codes)
      yield 'Nothing open\n\n'
      # if(datetime.datetime.now().month == endMonth):
      #   break
    # will cause thread to end
    print(term + " thread has been closed")
    return
  return Response(summer(), mimetype='text/event-stream')


@app.route("/spring", methods=['GET'])
def pthread():
  def spring():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    term = "1"
  # keep track of year, need to updates
    if month > 6:
      year +=1

    URL = finalURL = f'{baseURL}{year}&term={term}&campus=NB'
    print(term + str(year) + " thread has been opened")
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
        netid = mycursor.fetchone()
        id = row[0]
        codes = str(row[2])
        map = getCourseInfo(getCourses(term))
        courseName = map[codes]
        yield f'SnipeRU: {netid[0]}! {courseName}({codes}) opened!\n\n'
        notify.push(id, netid[0], courseName, codes)
        dbMethods.delCode(db, codes)
      yield 'Nothing open\n\n'
      # if(datetime.datetime.now().month == endMonth):
      #   break
    # will cause thread to end
    print(term + " thread has been closed")
    return
  return Response(spring(), mimetype='text/event-stream')

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
def getCourses(term):
  month = datetime.datetime.now().month
  print(month)
  year = datetime.datetime.now().year
  print(year)
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




      