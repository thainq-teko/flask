# -*- coding: utf-8 -*-
import flask
from flask import request, jsonify, make_response
from flask_cors import CORS

from flaskext.mysql import MySQL
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message

import random
import string

from config import configMail, configDB
from helpers import generateRandomPass
from repository import allRepos

import message


def create_app():
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
            return make_response(jsonify({'code': 400, 'message': message.USERNAME_REQUIRED}), 400)
        if not req["password"] or len(req["password"]) == 0:
            return make_response(jsonify({'code': 400, 'message': message.PASSWORD_REQUIRED}), 400)
        if not req["email"] or len(req["email"]) == 0:
            return make_response(jsonify({'code': 400, 'message': message.EMAIL_REQUIRED}), 400)

        name = req["username"]
        pw = req["password"]
        email = req['email']

        # check isExist username & email
        if len(allRepos.select_id_by_username(name)) > 0:
            return make_response(jsonify({'code': 400, 'message': message.ACOUNT_EXIST}), 400)
        if len(allRepos.select_id_by_email(email)) > 0:
            return make_response(jsonify({'code': 400, 'message': message.EMAIL_EXIST}), 400)

        pw_hashed = bcrypt.generate_password_hash(req["password"]).decode('utf-8').encode('ascii', 'ignore')

        record_for_inserting = (name, pw_hashed, email)
        allRepos.insert_for_register(record_for_inserting)

        msg = Message('Your account info', sender='accrac016@gmail.com', recipients=[email])
        msg.body = "username: " + name + " pass: " + pw
        mail.send(msg)
        return jsonify({'code': 200, 'message': message.CREATE_ACCOUNT})

    @app.route('/login', methods=['POST'])
    def login():
        # get body info
        req = request.get_json()
        name = req.get("username")
        pw = req.get("password")
        if not name or not pw or (not name and not pw):
            return make_response(jsonify({'code': 400, 'message': message.USERNAME_PASSWORD_REQUIRED}), 400)
        # check user exist
        if allRepos.select_user_by_username(name).rowcount == 0:
            return make_response(jsonify({'code': 400, 'message': message.USERNAME_NOT_FOUND}), 404)
        # check db
        cursor = allRepos.select_password_by_username(name)
        passInDb = cursor.fetchone()
        success = bcrypt.check_password_hash(passInDb[0], pw)
        if success:
            return make_response(jsonify({'code': 200, 'message': message.LOGIN_SUCCESS}), 200)
        return make_response(jsonify({'code': 400, 'message': message.WRONG_PASSWORD}), 400)

    @app.route('/forgotPass', methods=['POST'])
    def forgotPass():
        req = request.get_json()
        name = req.get("username")
        email = req.get("email")

        # handle body request
        if not name and not email:
            return make_response(jsonify({'code': 400, 'message': message.ALL_FIELDS_REQUIRED}), 400)
        if not name or len(name) == 0:
            return make_response(jsonify({'code': 400, 'message': message.USERNAME_REQUIRED}), 400)
        if not email or len(email) == 0:
            return make_response(jsonify({'code': 400, 'message': message.EMAIL_REQUIRED}), 400)
        # check username existed
        if allRepos.select_password_by_username(name).rowcount == 0:
            return make_response(jsonify({'code': 404, 'message': message.USERNAME_NOT_FOUND}), 404)
        # check email === username
        cursor = allRepos.select_email_by_username(name)
        fetchDB = cursor.fetchone()
        current = fetchDB[0].encode('ascii', 'ignore')
        if email != current:
            return make_response(jsonify({'code': 400, 'message': message.USERNAME_EMAIL_WRONG}), 400)
        # make new password for user
        new_pass = generateRandomPass.generatePassword(8)
        hashed_new_pass = bcrypt.generate_password_hash(new_pass)
        allRepos.update_password(hashed_new_pass, email)
        # handle mailing
        msg = Message('Password changed! ', sender='accrac016@gmail.com', recipients=['thainq00@gmail.com'])
        msg.body = "Your new password is: " + new_pass
        mail.send(msg)
        return make_response(jsonify({'code': 200, 'message': message.SEND_NEW_PASS}), 200)

    @app.route('/changePass', methods=['POST'])
    def changePass():
        req = request.get_json()
        name = req.get("username")
        pw = req.get("password")
        new_pw = req.get("newpassword")

        # handle body request
        if not name and not pw and not new_pw:
            return make_response(jsonify({'code': 400, 'message': message.ALL_FIELDS_REQUIRED}), 400)
        if not name or len(name) == 0:
            return make_response(jsonify({'code': 400, 'message': message.USERNAME_REQUIRED}), 400)
        if not pw or len(pw) == 0:
            return make_response(jsonify({'code': 400, 'message': message.PASSWORD_REQUIRED}), 400)
        if not new_pw or len(new_pw) == 0:
            return make_response(jsonify({'code': 400, 'message': message.NEW_PASSWORD_REQUIRED}), 400)

        passInDb = allRepos.select_password_by_username(name).fetchone()
        success = bcrypt.check_password_hash(passInDb[0], pw)
        if not success:
            return make_response(jsonify({'stt': 400, 'message': message.WRONG_USERNAME_PASSWORD}), 400)
        if pw == new_pw:
            return make_response(jsonify({'stt': 400, 'message': message.OLD_NEW_PASSWORD_DIFFERENT}),
                                 400)
        hashed_new_pass = bcrypt.generate_password_hash(new_pw)
        allRepos.update_password_by_username(hashed_new_pass, name)
        return make_response(jsonify({'code': 200, 'message': message.CHANGE_PASSWORD_SUCCESS}), 200)

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
