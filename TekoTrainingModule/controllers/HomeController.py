from TekoTrainingModule import app
from TekoTrainingModule.config import configMail
from TekoTrainingModule.repository import AuthRepository
from TekoTrainingModule.helpers import message
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from flask import request, jsonify, make_response

bcrypt = Bcrypt(app)
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
    if AuthRepository.get_id_by_username(name) is not None:
        return make_response(jsonify({'code': 400, 'message': message.ACOUNT_EXIST}), 400)
    if AuthRepository.get_id_by_email(email) is not None:
        return make_response(jsonify({'code': 400, 'message': message.EMAIL_EXIST}), 400)

    pw_hashed = bcrypt.generate_password_hash(req["password"]).decode('utf-8').encode('ascii', 'ignore')
    AuthRepository.add_user(name, email, pw_hashed)

    msg = Message('Your account info', sender='accrac016@gmail.com', recipients=[email])
    msg.body = "username: " + name + " pass: " + pw
    mail.send(msg)
    return jsonify({'code': 200, 'message': message.CREATE_ACCOUNT})
