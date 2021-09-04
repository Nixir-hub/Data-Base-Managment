# python3

import psycopg2
from psycopg2 import connect

connection = connect(
  host="localhost",
  user="postgres",
  password="coderslab",

)
connection.autocommit = True

def create_database():
    """
    Create database in psql
    :return: Database with table Users, Messages
    """
    while True:
        name = input("Write name of database and press ENTER:")
        cursor = connection.cursor()
        try:
            sql_code = "CREATE DATABASE " + name +"_db"
            cursor.execute(sql_code)
        except psycopg2.Error:
            print("Data base with this name already exist or wrong name.")
            continue

        def create_table1():
            """
            Create table user in created database
            :return:
            """
            connection = connect(
                host="localhost",
                user="postgres",
                password="coderslab",
                database=f"{name + '_db'}"
            )
            connection.autocommit = True
            cursor = connection.cursor()
            sql_code2 = "CREATE TABLE users(id serial PRIMARY KEY, username varchar(255) UNIQUE, hashed_password varchar(80)) "
            cursor.execute(sql_code2)
            return "Creating table users..."
        print(create_table1())
        def create_table2():
            """
            Create table message in created database
            :return:
            """
            connection = connect(
                host="localhost",
                user="postgres",
                password="coderslab",
                database=f"{name + '_db'}"
            )
            connection.autocommit = True
            cursor = connection.cursor()
            sql_code3 = """CREATE TABLE messages(
                            id SERIAL, 
                            from_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                            to_id INTEGER REFERENCES users(id) ON DELETE CASCADE, 
                            text varchar(255),
                            creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""
            cursor.execute(sql_code3)
            return "Adding table messages..."
        print(create_table2())

        return f"Database {name + '_db'} creation...Finished"
print(create_database())


