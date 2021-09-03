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
    :return:
    """
    while True:
        name = input("Write name of database and press ENTER:")
        cursor = connection.cursor()
        try:
            sql_code = "CREATE DATABASE " + name +"_db"
            cursor.execute(sql_code)
        except psycopg2.Error:
            print("Data base with this name arledy exist or wrong name.")
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
            sql_code2 = "CREATE TABLE users(id serial UNIQUE, username varchar(255), hashed_password varchar(80)) "
            cursor.execute(sql_code2)
            return "Created users table..."
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
            sql_code3 = """CREATE TABLE messages(id serial, form_id int NOT NULL, to_id int NOT NULL, creation_date timestamp, 
                                    text varchar(255)) """
            cursor.execute(sql_code3)
            return "Adding table messages..."
        print(create_table2())

        return f"Batabase {name + '_db'} creation...Finished"
print(create_database())


