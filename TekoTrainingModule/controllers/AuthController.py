from TekoTrainingModule import app
from TekoTrainingModule.repository import allRepos, AuthRepository
from TekoTrainingModule.helpers import message, generateRandomPass
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from flask import request, jsonify, make_response

mail = Mail(app)
bcrypt = Bcrypt(app)


@app.route('/login', methods=['POST'])
def login():
    # get body info
    req = request.get_json()
    name = req.get("username")
    pw = req.get("password")
    if not name or not pw or (not name and not pw):
        return make_response(jsonify({'code': 400, 'message': message.USERNAME_PASSWORD_REQUIRED}), 400)
    # check user exist
    if AuthRepository.get_user_by_username(name) is None:
        return make_response(jsonify({'code': 400, 'message': message.USERNAME_NOT_FOUND}), 404)
    # check db
    passInDb = AuthRepository.get_password_by_username(name)
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
    if AuthRepository.get_password_by_username(name) is None:
        return make_response(jsonify({'code': 404, 'message': message.USERNAME_NOT_FOUND}), 404)
    # check email === username
    fetchDB = AuthRepository.get_email_by_username(name)
    current = fetchDB[0].encode('ascii', 'ignore')
    if email != current:
        return make_response(jsonify({'code': 400, 'message': message.USERNAME_EMAIL_WRONG}), 400)
    # make new password for user
    new_pass = generateRandomPass.generatePassword(8)
    hashed_new_pass = bcrypt.generate_password_hash(new_pass)
    AuthRepository.forgot_pass(hashed_new_pass, email)
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

    passInDb = AuthRepository.get_password_by_username(name)
    success = bcrypt.check_password_hash(passInDb[0], pw)
    if not success:
        return make_response(jsonify({'stt': 400, 'message': message.WRONG_USERNAME_PASSWORD}), 400)
    if pw == new_pw:
        return make_response(jsonify({'stt': 400, 'message': message.OLD_NEW_PASSWORD_DIFFERENT}),
                             400)
    hashed_new_pass = bcrypt.generate_password_hash(new_pw)
    allRepos.update_password_by_username(hashed_new_pass, name)
    AuthRepository.change_pass(hashed_new_pass, name)
    return make_response(jsonify({'code': 200, 'message': message.CHANGE_PASSWORD_SUCCESS}), 200)
