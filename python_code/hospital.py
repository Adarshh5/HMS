import mysql.connector


class database:
    def __init__(self):
       self.mydb = mysql.connector.connect(
           host = "localhost",
           user = "root",
           password = "",
           database = "hospitalmanagementsystem"

       )
       self.mycursor = self.mydb.cursor()

obj = database()