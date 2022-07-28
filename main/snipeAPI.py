import os
import datetime
import re
# installed
from flask import Flask, jsonify, request, send_from_directory, Response
import json
import requests
import threading
import names
import time
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
term = termKey["fall"]
finalURL = f'{baseURL}{year}&term={term}&campus=NB'
print(finalURL)
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
  if netid is None:
    netid = names.get_first_name()
  print(netid)
  print(codes)
  if not(codes.isnumeric()):
    return "Non valid entry"
  # ADD FILTER FOR INPUTS
  filtered = re.sub(r'[^a-zA-Z0-9]', '', netid)
  courseDict = getCourseInfo(getCourses())
  print(filtered)
  if str(codes) not in courseDict:
    return "NON-VALID CODE, PLEASE TRY AGAIN"
  mycursor = db.cursor()
  mycursor.execute("ROLLBACK")
  dbMethods.addUser(db, filtered)
  dbMethods.addCode(db, codes, filtered)
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


@app.route("/stream", methods=['GET'])
def stream():
    print("push notif start", flush=True)
    def eventStream():
        count = 0
        while True:
            # Poll data from the database
            # and see if there's a new message
            today = datetime.date.today()
            count+=1
            yield f"event: notifications\ndata:{today}, {count}\n\n"
            time.sleep(1)
    
    return Response(eventStream(), mimetype='text/event-stream')

# @app.route("/stream", methods=['GET'])
# def stream():
#     print("push notif start", flush=True)
#     def monitorThread(term, endMonth, URL):
#       print(term + " thread has been opened")
#       # infinite loop until the registration period ends
#       while True:
#         var = False
        
#         # checks to see how long it will sleep until monitoring again
#         hour = datetime.datetime.now().hour
#         if hour < 6 or hour > 23:
#           min = datetime.datetime.now().minute
#           difference = 60 - crntMin
#           converted = difference * 60000
#           print("Hours is " + hour)
#           print("Sleeping ... waiting " + difference + " minutes")
#           sleep(converted)
#         # attempt to connect to the endpoint
#         while not(var):
#           try:
#               res = requests.get(URL)
#               var = True
#               # print("Connected")
#           except:
#               print("Failed to connect")

#         # creates a json object which is effectively a dictionary in python
#         openSections = res.json()
        
#         mycursor.execute("SELECT * FROM Codes")
#         course_codes = mycursor.fetchall()
#         # iterates through each row in the TABLE Codes
#         for row in course_codes:
#           if str(row[2]) not in openSections:
#             continue
#           # sends the row tuple which is: (id, uid, codes)
#           uid = row[1]
#           mycursor.execute("SELECT netid FROM Users WHERE uid = %s", (uid,))
#           netid = mycursor.fetchone()
#           id = row[0]
#           codes = str(row[2])
#           map = updateDB.getCourseInfo(updateDB.getCourses())
#           courseName = map[codes]
#           yield f'SnipeRU: {netid}! {courseName}({codes}) opened!\n\n'
#           # notify.push(id, netid[0], courseName, codes)
#           if(datetime.datetime.now().month == endMonth):
#             break
#       # will cause thread to end
#       print(term + " thread has been closed")
    
#     return Response(monitorThread("9", 17, finalURL), mimetype='text/event-stream')


def buildMessage(id, netid, courseName, codes, URL, email):
    subject = f'SnipeRU: {netid}! {courseName}({codes}) opened!'
    message = Mail(
    from_email='sniperuapp@gmail.com',
    to_emails=email,
    subject=subject,
    html_content=URL)
    return message


# need to add option to opt-in to email, currently it is the default method
def push(id, netid, courseName, codes):
    # sends email
    year = datetime.datetime.now().year
    print(year)
    finalURL = f'{pushURL}{getTerm()}{year}&indexList={codes}'
    email = dbMethods.getEmail(db, netid)
    if email[0] is None:
        # send push notification
        print("hello")
    else:
        message = buildMessage(id, netid, courseName, codes, finalURL, email[0])
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)
    dbMethods.delCode(db, codes)










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

if __name__ == "__main__":
    app.run()