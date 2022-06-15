import mysql.connector
from mysql.connector import errorcode

def connect():
  var = False
  while not(var):
    try:
        db = mysql.connector.connect(
        user='root',
        password = 'TO_BE_REPLACED_WITH_REAL_PASSWORD',
        database='course_codes'
        )
        print("Connected to MySQL DB")
        var = True
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
        return
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
        return
      else:
        print(err)

  return db

def addUser(db, netid):
  try:
      mycursor = db.cursor()
      mycursor.execute("INSERT INTO Users (netid) VALUES (%s)", (netid,))
      db.commit()
      print("Successfully added user " + netid)
      var = True
  except mysql.connector.IntegrityError as err:
      if err.errno == 1062:
          print("DUPLICATE USER, ALREADY EXISTS")

def addCode(db, code, netid):
  try:
      mycursor = db.cursor()
      Q =  "INSERT INTO Codes\
            SET codes = %s,\
            uid = (SELECT uid\
            FROM Users\
            WHERE netid = %s)"
      pair = (code, netid)
      mycursor.execute(Q, pair)
      db.commit()
  
      print("Successfully added " + str(pair[0]) + " " + pair[1])
      var = True
  except mysql.connector.IntegrityError as err:
      if err.errno == 1062:
          print("CODE ALREADY ADDED")

def delCode(db, code):
  # Don't have to use try catch here because no errors are thrown when deleting a non empty thing
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


