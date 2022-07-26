import connect

db = connect.connect()
mycursor = db.cursor()
mycursor.execute("Show tables;")
myresult = mycursor.fetchall()
db.close()
for x in myresult:
    print(x)


def food():
    print("FOO")