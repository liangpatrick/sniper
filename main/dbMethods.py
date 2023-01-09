import psycopg2 
import sys
import os

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

def addUser(db, netid):
  try:
    mycursor = db.cursor()
    mycursor.execute("INSERT INTO Users (netid) VALUES (%s)", (netid,))
    db.commit()
    print("Successfully added user " + netid)
    return "Successfully added user " + netid
  except psycopg2.errors.UniqueViolation as err:
    print("DUPLICATE USER, ALREADY EXISTS")
    return "User already added."

def addEmail(db, netid, email):
  try:
    mycursor = db.cursor()
    mycursor.execute("UPDATE Users SET email = %s WHERE netid = %s", (email, netid))
    db.commit()
    print("Successfully added " + email + " for " + netid)
    return("Successfully added " + email + " for " + netid)
  except psycopg2.errors.CheckViolation as err:
    print(err)
    return "Invalid email address, please try again."

  

def addCode(db, code, netid, term):
  try:
      mycursor = db.cursor()
      mycursor.execute("SELECT uid FROM Users WHERE netid = %s", (netid,))
      uid = mycursor.fetchall()
      Q =  "INSERT INTO Codes (codes, uid, term)\
            VALUES (%s,%s, %s)"
      pair = (code, (uid[0],), term)
      mycursor.execute(Q, pair)
      db.commit()
  
      print("Successfully added " + str(pair[0]) + " " + netid)
      var = True
  except psycopg2.errors.UniqueViolation as err:
    print("CODE ALREADY ADDED")

def delCode(db, code):
  # Don't have to use try catch here because no errors are thrown when deleting a non existing thing
  mycursor = db.cursor()
  Q = "DELETE FROM Codes WHERE codes = %s"
  dele = (code,)
  mycursor.execute(Q, dele)
  db.commit()
  print("Successfully removed " + str(dele[0]))
  var = True
  
def getEmail(db, netid):
  mycursor = db.cursor()
  mycursor.execute("SELECT email FROM Users WHERE netid = %s", (netid,))
  email = mycursor.fetchone()
  return email


def showUsers(db):
  mycursor = db.cursor()
  mycursor.execute("SELECT * FROM Users")

  result = mycursor.fetchall()

  for x in result:
    print(x)

def showCodes(db):
  mycursor = db.cursor()
  mycursor.execute("SELECT * FROM Codes")

  result = mycursor.fetchall()

  for x in result:
    print(x)

# showUsers(connect())
# showCodes(connect())


# mycursor.execute("Show tables;")
 
# myresult = mycursor.fetchall()
 
# for x in myresult:
#     print(x)


