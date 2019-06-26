from TekoTrainingModule import app
from flask import request, jsonify, make_response

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
