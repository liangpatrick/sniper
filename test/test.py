# import foo
import requests
# var = True
# print(bool(var))
import re, string
import os.path
import psycopg2 
import sys
import os
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# test string formatter
# baseURL = "http://sis.rutgers.edu/soc/api/openSections.json?year="
# year = 2022
# termKey= {
#     'winter': 0,
#     'spring': 1,
#     'summer': 7,
#     'fall': 9
# }
# term = termKey["summer"]
# finalURL = f'{baseURL}{year+1}&term={term}&campus=NB'
# print(finalURL)
# var = False
# # while not(var):
# try:
#     res = requests.get(finalURL)
#     var = True
#     print("Connected")
# except:
#     print("Failed to connect")
# # openSections = res.json()
# # if "01141" in openSections:
# #     print("open")
# # fool = foo.food()
# # fool

# input = "pzl_4"
 
# s = re.sub(r'[^a-zA-Z0-9]', '', input)
# print(s)

def connect():
  var = False
  while not(var):
    try:
      DATABASE_URL = os.environ['DATABASE_URL']
      db = psycopg2.connect(DATABASE_URL, sslmode='require')
      print("Connected to PostgreSQL DB")
      var = True
    except psycopg2.OperationalError as err:
        print(err)

  return db

netid = "pzl4"
email = "liangpatrick1234-@gmail.com"


db = connect()
# try:
#     mycursor = db.cursor()
#     mycursor.execute("UPDATE Users SET email = %s WHERE netid = %s", (email, netid))
#     db.commit()
#     print("Successfully added " + email + " to " + netid)
# except psycopg2.errors as err:
#     if err.errno == errorcode.CheckViolation:
#         print("hello")
#     print(err)

mycursor = db.cursor()
mycursor.execute("SELECT * FROM Codes")

result = mycursor.fetchall()

for x in result:
  print(x[2])


# SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


# def main():
#     """Shows basic usage of the Gmail API.
#     Lists the user's Gmail labels.
#     """
#     creds = None
#     # The file token.json stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists('token.json'):
#         creds = Credentials.from_authorized_user_file('token.json', SCOPES)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())

#     try:
#         # Call the Gmail API
#         service = build('gmail', 'v1', credentials=creds)
#         results = service.users().labels().list(userId='me').execute()
#         labels = results.get('labels', [])

#         if not labels:
#             print('No labels found.')
#             return
#         print('Labels:')
#         for label in labels:
#             print(label['name'])

#     except HttpError as error:
#         # TODO(developer) - Handle errors from gmail API.
#         print(f'An error occurred: {error}')


# if __name__ == '__main__':
#     main()