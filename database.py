import mysql.connector

config = {
    'user': 'root',
    'passwd': 'password22',
    'host': '127.0.0.1',
    'raise_on_warnings': True
}

db = mysql.connector.connect(**config)
cursor = db.cursor()