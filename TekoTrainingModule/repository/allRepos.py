import pymysql

from TekoTrainingModule.config import configDB

db = pymysql.connect(configDB.host, configDB.name, configDB.passw, configDB.db)


def select_id_by_username(username):
    cursor = db.cursor()
    cursor.execute("select id from user where username = %s", username)
    results = cursor.fetchall()
    return results


def select_id_by_email(email):
    cursor = db.cursor()
    cursor.execute("select id from user where email = %s", email)
    results = cursor.fetchall()
    return results


def insert_for_register(params):
    cursor = db.cursor()
    cursor.execute("Insert into user (username, password, email) values (%s, %s, %s)", params)
    db.commit()
    return 1


def select_user_by_username(username):
    cursor = db.cursor()
    cursor.execute("Select * from user where username = %s", username)
    return cursor


def select_password_by_username(username):
    cursor = db.cursor()
    cursor.execute("Select password from user where username = %s", username)
    return cursor


def select_email_by_username(username):
    cursor = db.cursor()
    cursor.execute("Select email from user where username = %s", username)
    return cursor


def update_password(hash_pw, email):
    cursor = db.cursor()
    cursor.execute("update user set password = %s where email = %s", (hash_pw, email))
    db.commit()
    return 1


def update_password_by_username(hash_pw, username):
    cursor = db.cursor()
    cursor.execute("update user set password = %s where username = %s", (hash_pw, username))
    db.commit()
    return 1
