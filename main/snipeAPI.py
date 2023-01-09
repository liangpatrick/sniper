import os
import datetime
import re
# installed
from flask import Flask, jsonify, request, send_from_directory, Response
import json
import requests
import names
import time
# import gevent
import psycopg2 
# own files
import dbMethods

# Create Flask object
app = Flask(__name__)

baseURL = "http://sis.rutgers.edu/soc/api/openSections.json?year="
# rest of the URL template: {year}&term={term}&campus=NB
courseURL = "https://sis.rutgers.edu/soc/api/courses.json?year="
# rest of the URL template: {year}&term={term}&campus=NB
# connect to sql database
db = dbMethods.connect()

# db = psycopg2.connect(
#     host="localhost",
#     user='liangpatrick',
#     password = 'PostSQL2#$',
#     database='course_codes'
# )

mycursor = db.cursor()


# key bindings for terms
termKey= {
    'summer': 7,
    'winter': 0,
    'fall': 9,
    'spring': 1 
}
year = datetime.datetime.now().year
  # print(year)
  # only happens once a month and at 6 am
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

# wrapper method for dbMethods
# updates sql DB and front end will always push the netid
# Endpoint that will only accept POST requests
@app.route("/addCode", methods=['POST'])
def updateDB():
  params = request.get_json()
  netid = params["netid"]
  codes = params["codes"]
  season = params["season"]
  if netid is None:
    netid = names.get_first_name()
  print(netid)
  print(codes)
  print(season)
  if not(codes.isnumeric()):
    return "Non valid entry"
  # ADD FILTER FOR INPUTS
  filtered = re.sub(r'[^a-zA-Z0-9]', '', netid)
  courseDict = getCourseInfo(getCourses(season))
  print(filtered)
  if str(codes) not in courseDict:
    return "NON-VALID CODE, PLEASE TRY AGAIN"
  mycursor = db.cursor()
  mycursor.execute("ROLLBACK")
  dbMethods.addUser(db, filtered)
  dbMethods.addCode(db, codes, filtered,termKey[season])
  # dbMethods.showCodes(db)
  # dbMethods.delCode(db, "05386")
  # dbMethods.showCodes(db)
  print("Success")
  return "Success"

@app.route("/addEmail", methods=['POST'])
def addEmail():
  params = request.get_json()
  netid = params["netid"]
  email = params["email"]
  return dbMethods.addEmail(db, netid, email)



if __name__ == "__main__":
    app.run()