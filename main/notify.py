import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
import datetime
import re

import requests
# own files
import dbMethods

pushURL = "http://sims.rutgers.edu/webreg/editSchedule.htm?login=cas&semesterSelection="
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
