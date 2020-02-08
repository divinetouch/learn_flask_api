import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)'
cursor.execute(create_table)

create_table = 'CREATE TABLE IF NOT EXISTS items (name text, price real)'
cursor.execute(create_table)

cursor.execute('INSERT INTO users VALUES(NULL, "divine", "asdf")')
cursor.execute('INSERT INTO items VALUES("chair", 10.99)')
cursor.execute('INSERT INTO items VALUES("table", 20.99)')
cursor.execute('INSERT INTO items VALUES("mirror", 15.99)')

connection.commit()

connection.close()
