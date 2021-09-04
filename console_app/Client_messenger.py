# python3

import argparse
from models import Message, User
from clcrypto import check_password
from psycopg2 import connect, OperationalError


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="input username")
parser.add_argument("-p", "--password", help="input password")
parser.add_argument("-t", "--to", help="choose to who you wat to send this message")
parser.add_argument("-s", "--send", help="send message to the [-t]")
parser.add_argument("-ml", "--messageslist", action="store_true", help="show list of messages")
parser.add_argument("-ul", "--userslist", action="store_true", help="show list of users")

args = parser.parse_args()


def list_of_users(cursor):
    """
    check database for users
    :param cur: takes cursor parm
    :return: list of users
    """
    users = User.load_all_users(cursor)
    for user in users:
        print(user.username)


def user_check(cursor, username, passw):
    user = User.load_user_by_username(cursor, username)
    if not user:
        print("User does not exist!")
        return False
    elif check_password(passw, user.hashed_password):
        print("Password correct.")
    else:
        return False


def list_of_messages(cursor):
    messages = Message.load_all_messages(cursor)
    for message in messages:
        print(f"To: {message.to_id}, From {message.from_id}, Text: {message.text} time:{message._creation_data}")


def send_message(cur, from_id, recipient_name, text):

    if len(text) > 255:
        print("Message is too long!")
        return
    to = User.load_user_by_username(cur, recipient_name)
    if to:
        message = Message(from_id, to.id, text=text)
        message.save_to_db(cur)
        print("Message send")
    else:
        print("Recipient does not exists.")

if __name__ == '__main__':
    try:
        connection = connect(database="workshop_db", user="postgres", password="coderslab", host="127.0.0.1")
        connection.autocommit = True
        cursor = connection.cursor()
        if args.username and args.password:
            user = User.load_user_by_username(cursor, args.username)
            if check_password(args.password, user.hashed_password):
                if args.messageslist:
                    list_of_messages(cursor)
                elif args.to and args.send:
                    send_message(cursor, user.id, args.to, args.send)
                else:
                    print("Send to username isn't possible. Username doesn't exist.")
            else:
                print("Wrong username or password!")

        connection.close()
    except OperationalError as problem2:
        print("Connection Error: ", problem2)