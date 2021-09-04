# python3

import argparse
from models import User
from clcrypto import check_password
from psycopg2 import connect, OperationalError
from psycopg2.errors import UniqueViolation


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="input username")
parser.add_argument("-p", "--password", help="input password")
parser.add_argument("-n", "--new_pass", help="set new password")
parser.add_argument("-l", "--list", action="store_true", help="show list of users")
parser.add_argument("-d", "--delete", action="store_true", help="delete user")
parser.add_argument("-e", "--edit", action="store_true", help="edit user")
args = parser.parse_args()


def list_users(item):
    """
    check database for users
    :param cur: takes cursor parm
    :return:
    """
    users = User.load_all_users(item)
    for user in users:
        print(user.username)


def edit_user(item, username, pword, npass):
    """
    change users information
    :param item: takes cursor parm
    :param username: takes username from console
    :param pword: takes pword from console
    :param npass: takes new password from console
    :return: string or change user password
    """
    user = User.load_user_by_username(item, username)
    if not user:
        print("User does not exist!")
    elif check_password(pword, user.hashed_password):
        if len(npass) < 8:
            print("Password is to short. It should have minimum 8 characters.")
        else:
            user.hashed_password = npass
            user.save_to_db(item)
            print("Password changed.")
    else:
        print("Incorrect password")


def create_user(item, username, passw):
    """
    Check username table and if user doesn't exist create username and set password
    :param item: takes cursor parm
    :param username:
    :param passw: password
    :return: str if something gone wrong or create user
    """
    if len(passw) < 8:
        print("To short. Password should have minimum 8 characters.")
    else:
        try:
            user = User(username=username, password=passw)
            user.save_to_db(item)
            print("User created")
        except UniqueViolation as problem1:
            print("User already exist. Pick other username. ", problem1)


def del_user(item, username, passw):
    """
    Delete user form database
    :param item: takes cursor parm
    :param username:
    :param passw:
    :return: if user exist delete it from database
    """
    user = User.load_user_by_username(item, username)
    if not user:
        print("User does not exist!")
    elif check_password(passw, user.hashed_password):
        user.delete(item)
        print("User deleted.")
    else:
        print("Incorrect password!")


if __name__ == '__main__':
    try:
        connection = connect(database="workshop_db", user="postgres", password="coderslab", host="127.0.0.1")
        connection.autocommit = True
        cursor = connection.cursor()
        if args.username and args.password and args.edit and args.new_pass:
            edit_user(cursor, args.username, args.password, args.new_pass)
        elif args.username and args.password and args.delete:
            del_user(cursor, args.username, args.password)
        elif args.username and args.password:
            create_user(cursor, args.username, args.password)
        elif args.list:
            list_users(cursor)
        else:
            parser.print_help()
        connection.close()
    except OperationalError as problem2:
        print("Connection Error: ", problem2)
