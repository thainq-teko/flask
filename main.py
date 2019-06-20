# -*- coding: utf-8 -*-
import flask
from flask import request, jsonify, make_response
from flask_cors import CORS

from flaskext.mysql import MySQL
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message

import random
import string

import os
import configDB
import heroku
import configMail


def create_app(config=None):
    app = flask.Flask(__name__)
    app.config["DEBUG"] = True

    CORS(app)
    bcrypt = Bcrypt(app)
    mysql = MySQL()

    # config mysql connection
    app.config['MYSQL_DATABASE_USER'] = configDB.name
    app.config['MYSQL_DATABASE_PASSWORD'] = configDB.passw
    app.config['MYSQL_DATABASE_DB'] = configDB.db
    app.config['MYSQL_DATABASE_HOST'] = configDB.host

    # config db using heroku clearDB
    # app.config['MYSQL_DATABASE_USER'] = heroku.name
    # app.config['MYSQL_DATABASE_PASSWORD'] = heroku.passw
    # app.config['MYSQL_DATABASE_DB'] = heroku.db
    # app.config['MYSQL_DATABASE_HOST'] = heroku.host

    mysql.init_app(app)

    conn = mysql.connect()
    pointer = conn.cursor()

    # config flask_mail
    mail = Mail(app)
    app.config['MAIL_SERVER'] = configMail.mail_server
    app.config['MAIL_PORT'] = configMail.mail_port
    app.config['MAIL_USERNAME'] = configMail.username
    app.config['MAIL_PASSWORD'] = configMail.password
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail = Mail(app)

    @app.route('/', methods=['GET'])
    def home():
        return "Hello, flask app works ! - Thainq"

    @app.route('/register', methods=['POST'])
    def register():
        req = request.get_json()
        # handle body request
        if not req["username"] or len(req["username"]) == 0:
            return make_response(jsonify({'code': 400, 'message': "username required!"}), 400)
        if not req["password"] or len(req["password"]) == 0:
            return make_response(jsonify({'code': 400, 'message': "password required!"}), 400)
        if not req["email"] or len(req["email"]) == 0:
            return make_response(jsonify({'code': 400, 'message': "email required!"}), 400)

        # get body request

        name = req["username"]
        pw = req["password"]
        email = req['email']
        print(name, pw, email)
        pw_hashed = bcrypt.generate_password_hash(req["password"]).decode('utf-8').encode('ascii', 'ignore')

        # validate body request

        # check isExist username & email
        pointer.execute("select id from user where username = %s", name)
        if len(pointer.fetchall()) > 0:
            return make_response(jsonify({'code': 400, 'message': "account existed!"}), 400)
        pointer.execute("select id from user where email = %s", email)
        if len(pointer.fetchall()) > 0:
            return make_response(jsonify({'code': 400, 'message': "email existed!"}), 400)

        # sql query for inserting data
        record_for_inserting = (name, pw_hashed, email)
        sql = "Insert into user (username, password, email) values (%s, %s, %s)"
        # print(record_for_inserting)
        pointer.execute(sql, record_for_inserting)
        conn.commit()

        # handle mailing

        msg = Message('Your account info', sender='accrac016@gmail.com', recipients=['thainq00@gmail.com'])
        msg.body = "username: " + name + " pass: " + pw
        mail.send(msg)
        return jsonify({'code': 200, 'message': "create account successfully"})

    @app.route('/login', methods=['POST'])
    def login():
        # get body info
        req = request.get_json()
        name = req.get("username")
        pw = req.get("password")
        if not name or not pw or (not name and not pw):
            return make_response(jsonify({'code': 400, 'message': "Both username anhd password are required!"}), 400)
        # check user exist
        pointer.execute("Select * from user where username = %s", name)
        if pointer.rowcount == 0:
            return make_response(jsonify({'code': 400, 'message': "Username not found"}), 404)
        # check db
        pointer.execute("Select password from user where username = %s", name)
        passInDb = pointer.fetchone()
        success = bcrypt.check_password_hash(passInDb[0], pw)
        if success:
            return make_response(jsonify({'code': 200, 'message': "login success"}), 200)
        return make_response(jsonify({'code': 400, 'message': "wrong password"}), 400)

    # func for creating password
    def generatePassword(length):
        numStr = ''.join(random.choice(string.digits) for _ in range(2))
        charStr = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(length - 2))
        return charStr[-6:-2] + numStr + charStr[-2:]

    @app.route('/forgotPass', methods=['POST'])
    def forgotPass():
        req = request.get_json()
        name = req.get("username")
        email = req.get("email")

        # handle body request
        if not name and not email:
            return make_response(jsonify({'code': 400, 'message': "All fields required!"}), 400)
        if not name or len(name) == 0:
            return make_response(jsonify({'code': 400, 'message': "username required!"}), 400)
        if not email or len(email) == 0:
            return make_response(jsonify({'code': 400, 'message': "email required!"}), 400)
        # check username existed
        pointer.execute("Select * from user where username = %s", name)
        if pointer.rowcount == 0:
            return make_response(jsonify({'code': 404, 'message': 'username not found!'}), 404)
        # check email === username
        pointer.execute("Select email from user where username = %s", name)
        fetchDB = pointer.fetchone()
        current = fetchDB[0].encode('ascii', 'ignore')
        if email != current:
            return make_response(jsonify({'code': 400, 'message': 'user and email not belong together!'}), 400)
        # make new password for user
        new_pass = generatePassword(8)
        hashed_new_pass = bcrypt.generate_password_hash(new_pass)
        pointer.execute("update user set password = %s where email = %s",
                        (hashed_new_pass.decode('utf-8').encode('ascii', 'ignore'), email))
        conn.commit()
        # handle mailing
        msg = Message('Password changed! ', sender='accrac016@gmail.com', recipients=['thainq00@gmail.com'])
        msg.body = "Your new password is: " + new_pass
        mail.send(msg)
        return make_response(jsonify({'code': 200, 'message': 'New password sent to your mail!'}), 200)

    @app.route('/changePass', methods=['POST'])
    def changePass():
        req = request.get_json()
        name = req.get("username")
        pw = req.get("password")
        new_pw = req.get("newpassword")

        # handle body request
        if not name and not pw and not new_pw:
            return make_response(jsonify({'code': 400, 'message': "All fields required!"}), 400)
        if not name or len(name) == 0:
            return make_response(jsonify({'code': 400, 'message': "username required!"}), 400)
        if not pw or len(pw) == 0:
            return make_response(jsonify({'code': 400, 'message': "password required!"}), 400)
        if not new_pw or len(new_pw) == 0:
            return make_response(jsonify({'code': 400, 'message': "new password required!"}), 400)
        pointer.execute("Select password from user where username = %s", name)
        passInDb = pointer.fetchone()
        success = bcrypt.check_password_hash(passInDb[0], pw)
        if not success:
            return make_response(jsonify({'stt': 400, 'message': "wrong username or password"}), 400)
        if pw == new_pw:
            return make_response(jsonify({'stt': 400, 'message': "old password and new password must be different"}),
                                 400)
        hashed_new_pass = bcrypt.generate_password_hash(new_pw)
        pointer.execute("update user set password = %s where username = %s",
                        (hashed_new_pass.decode('utf-8').encode('ascii', 'ignore'), name))
        conn.commit()
        return make_response(jsonify({'code': 200, 'message': 'Change password successfully!'}), 200)

    @app.route('/delete_for_testing', methods=['POST'])
    def delete():
        req = request.get_json()
        name = req["username"]
        pointer.execute("delete from user where username = %s", name)
        conn.commit()
        return make_response(jsonify({'code': 200, 'message': request.get_json()}), 200)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
