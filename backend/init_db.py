# Add the necessary imports
import mysql.connector as mysql
import os
import datetime
from dotenv import load_dotenv

''' Environment Variables '''
load_dotenv("credentials.env")

# Read Database connection variables
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']

# Connect to the db and create a cursor object
db = mysql.connect(user=db_user, password=db_pass, host=db_host)
cursor = db.cursor()

cursor.execute("CREATE DATABASE if not exists leaderboard")
cursor.execute("USE leaderboard")
cursor.execute("DROP TABLE IF EXISTS users;")
cursor.execute("DROP TABLE IF EXISTS comments;")

try:
    cursor.execute("""
        CREATE TABLE users (
          id INT AUTO_INCREMENT PRIMARY KEY,
          username VARCHAR(25) NOT NULL UNIQUE,
          first_name VARCHAR(50) NOT NULL,
          last_name VARCHAR(50) NOT NULL,
          student_id CHAR(8) NOT NULL,
          email VARCHAR(50) NOT NULL UNIQUE,
          hashed_password VARCHAR(100) NOT NULL
        );
    """)
    cursor.execute("""
        CREATE TABLE comments (
          id INT AUTO_INCREMENT PRIMARY KEY,
          username VARCHAR(50) NOT NULL,
          comment VARCHAR(500) NOT NULL,
          comment_id VARCHAR(50) NOT NULL,
          date VARCHAR(50) NOT NULL
        );
    """)
except mysql.Error as err:
    print("MySQL error: {0}".format(err))

# Populate Users table with a single user
try:
    query = "INSERT INTO users (username, first_name, last_name, email, student_id, hashed_password) VALUES (%s, %s, %s, %s, %s, %s)"
    values = [
        ('johndoe', 'John', 'Doe', 'johndoe@example.com', '12345678', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW'),
    ]
    cursor.executemany(query, values)

    db.commit()
except mysql.Error as err:
    print("MySQL error: {0}".format(err))
    db.rollback()

# Populate comments table with comments
try:
    query = "INSERT INTO comments (username, comment, comment_id, date) VALUES (%s, %s, %s, %s)"
    values = [
        ('johndoe', 'Wow, what a great idea!', '1', '16 March 2023, at 10:10 PM'),
    ]
    cursor.executemany(query, values)
    db.commit()
except mysql.Error as err:
    print("MySQL error: {0}".format(err))
    db.rollback()


# Close the cursor and database connection
cursor.close()
db.close()
