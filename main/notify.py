import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
import datetime
import re

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

def getEmail():
    print("hello")


def buildMessage(id, netid, courseName, codes, URL):
    # message = Mail()
    # message.to = [
    #     To(
    #         email="liangpatrick1234@gmail.com",
    #         name="pzl4",
    #         p=0
    #     ),
    # ]

    # message.from_email = From(
    #     email="sniperuapp@gmail.com",
    #     name="SnipeRU",
    #     p=1
    # )
    # subject = f'SnipeRU: {netid}! {codes} opened!'
    # message.subject = Subject(subject)

    # message.content = [
    #     Content(
    #         mime_type="text/html",
    #         content="<p>Hello from Twilio SendGrid!</p><p>Sending with the email service trusted by developers and marketers for <strong>time-savings</strong>, <strong>scalability</strong>, and <strong>delivery expertise</strong>.</p><p>%open-track%</p>"
    #     )
    # ]


    # message.asm = Asm(
    #     group_id=GroupId(12345),
    #     groups_to_display=GroupsToDisplay([12345])
    # )

    # message.ip_pool_name = IpPoolName("transactional email")

    # message.mail_settings = MailSettings(
    #     bypass_list_management=BypassListManagement(False),
    #     footer_settings=FooterSettings(False),
    #     sandbox_mode=SandBoxMode(False)
    # )

    # message.tracking_settings = TrackingSettings(
    #     click_tracking=ClickTracking(
    #         enable=True,
    #         enable_text=False
    #     ),
    #     open_tracking=OpenTracking(
    #         enable=True,
    #         substitution_tag=OpenTrackingSubstitutionTag("%open-track%")
    #     ),
    #     subscription_tracking=SubscriptionTracking(False)
    # )
    subject = f'SnipeRU: {netid}! {courseName}({codes}) opened!'
    message = Mail(
    from_email='sniperuapp@gmail.com',
    to_emails='liangpatrick1234@gmail.com',
    subject=subject,
    html_content=URL)
    return message


# need to add option to opt-in to email, currently it is the default method
def push(id, netid, courseName, codes):
    # sends email
    year = datetime.datetime.now().year
    print(year)
    finalURL = f'{baseURL}{getTerm()}{year}&indexList={codes}'

    message = buildMessage(id, netid, courseName, codes, finalURL)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
    dbMethods.delCode(db, codes)
