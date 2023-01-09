import psycopg2

try:
    db = psycopg2.connect(
        host="localhost",
        user='liangpatrick',
        password = 'PostSQL2#$',
        database='course_codes'
    )
    print("Connected to PostgreSQL DB")
    var = True
except psycopg2.OperationalError as err:
    print(err)
# db.close()