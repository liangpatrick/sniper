import psycopg2 
import sys
# mycursor = db.cursor()

def connect():
  var = False
  while not(var):
    try:
      DATABASE_URL = ''
      
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
  except psycopg2.errors.UniqueViolation as err:
    print("DUPLICATE USER, ALREADY EXISTS")

def addCode(db, code, netid):
  try:
      mycursor = db.cursor()
      mycursor.execute("SELECT uid FROM Users WHERE netid = %s", (netid,))
      uid = mycursor.fetchall()
      Q =  "INSERT INTO Codes (codes, uid)\
            VALUES (%s,%s)"
      pair = (code, (uid[0],))
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


