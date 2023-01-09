# installed
import os
import psycopg2

try:
  DATABASE_URL = os.environ['DATABASE_URL']
  
  db = psycopg2.connect(DATABASE_URL, sslmode='require')
  print("Connected to PostgreSQL DB")
  var = True
except psycopg2.OperationalError as err:
    print(err)

    
# print(os.environ)
# DATABASE_URL = 'postgres://aezoqicdyvmfpv:9e122cf1d32771e5cb83111839a4136759aeff644d817c7a2d39c4f359a0f302@ec2-52-20-166-21.compute-1.amazonaws.com:5432/d1sonj4hukngri'

# db = psycopg2.connect(DATABASE_URL, sslmode='require')

db = psycopg2.connect(
    host="localhost",
    user='liangpatrick',
    password = 'PostSQL2#$',
    database='course_codes'
)
mycursor = db.cursor()

# UPDATE LENGTH INPUT


# Create tables
# might add a phone number column
# mycursor.execute("CREATE TABLE Users (uid SERIAL PRIMARY KEY, netid VARCHAR(50) NOT NULL UNIQUE)")
# mycursor.execute("CREATE TABLE Codes (id SERIAL PRIMARY KEY, uid INT, FOREIGN KEY( uid) REFERENCES Users (uid), codes INT NOT NULL UNIQUE)")
# db.commit()

# Test tables

# Q1 = "INSERT INTO Codes (id, codes) VALUES (%s, %s)"
# last_id = mycursor.lastrowid

# example of how i should add things to the sql server, must get lastrowid and store it as a constant
# code = (last_id, 1234)
# mycursor.execute(Q1, code)
# db.commit()

# try:
#     mycursor.execute("INSERT INTO Users (netid) VALUES ('pzl4')")
#     db.commit()
#     print("Successfully added user " + 'pzl4')
#     var = True
# except psycopg2.errors.UniqueViolation as err:
#   print("DUPLICATE USER, ALREADY EXISTS")
# db.commit()
# Q1 = "INSERT INTO Codes (id, codes) VALUES (%s, %s)"
# last_id = mycursor.lastrowid
# print(last_id)
# # example of how i should add things to the sql server, must get lastrowid and store it as a constant
# code = (2, 1234)
# mycursor.execute(Q1, code)
# db.commit()

# ONLY IN MYSQL, NOT POSTGRES
# Q2 = "INSERT INTO Codes \
#         SET codes = %s,\
#        uid = (\
#        SELECT uid\
#          FROM Users\
#         WHERE netid = %s)"
# mycursor.execute("SELECT uid FROM Users WHERE netid = %s", ("pzl4",))
# myresult = mycursor.fetchall()
# print(myresult)
# Q2 = "INSERT INTO Codes (codes, uid)\
#         VALUES(%s,\
#         SELECT uid\
#         FROM Users\
#         WHERE netid = %s)"


# pair = (12, "pzl4")
# mycursor.execute(Q2, pair)
# db.commit()

# delete
# mycursor.execute("DELETE FROM Users WHERE netid = 'pzl4'")
# db.commit()

s = "SELECT table_schema, table_name FROM information_schema.tables WHERE ( table_schema = 'public' ) ORDER BY table_schema, table_name;"
mycursor.execute(s)
myresult = mycursor.fetchall()
 
for x in myresult:
    print(x)

# iterates through each table to show whats in the table
print("\nUsers:")
mycursor.execute("SELECT * FROM Users")

result = mycursor.fetchall()

for x in result:
  print(x)

print("Codes:")
mycursor.execute("SELECT * FROM Codes")

res = mycursor.fetchall()

for x in res:
  print(x)
    
db.close()