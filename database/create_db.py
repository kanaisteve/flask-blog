from mysql.connector import errorcode
from database import cursor

# DB_NAME = 'users'

cursor.execute("CREATE DATABASE flskr_users")
cursor.execute("SHOW DATABASES")

for db in cursor:
    print(db)