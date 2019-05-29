# -*- coding: utf-8 -*-
import flask
from flask import request, jsonify, json
from flask_cors import CORS

from flaskext.mysql import MySQL
from flask_bcrypt import Bcrypt 
from flask_mail import Mail, Message

app = flask.Flask(__name__)
app.config["DEBUG"] = True

CORS(app)
bcrypt = Bcrypt(app)
mysql = MySQL()

# config mysql connection
app.config['MYSQL_DATABASE_USER'] = 'teko'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
app.config['MYSQL_DATABASE_DB'] = 'flask_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
pointer = conn.cursor()

# config flask_mail
mail = Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'accrac016@gmail.com'
app.config['MAIL_PASSWORD'] = 'pa5512!@'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
'''
@app.route('/allUser', methods=['GET'])
def all_user():
    pointer.execute("SELECT * FROM user")
    data = pointer.fetchall()
    result = []
    for i in data :
        result.append({
            'id' : i[0],
            'name': i[1].encode('ascii','ignore') #convert unicode to string
        })
    return jsonify(result)
'''
@app.route('/register', methods=['POST'])
def register():
    req = request.get_json()
    name = req["username"]
    pw = req["password"]
    pw_hashed = bcrypt.generate_password_hash(req["password"]).decode('utf-8').encode('ascii', 'ignore')
    email = req['email'].encode('ascii', 'ignore')
    # check isExist username & email
    pointer.execute("select id from user where username = %s", str(name))
    if len(pointer.fetchall()) > 0:
        return jsonify({'code': 401, 'message': "account existed!"})
    pointer.execute("select id from user where email = %s", str(email))
    if len(pointer.fetchall()) > 0:
        return jsonify({'code': 401, 'message': "email existed!"})
    # sql query
    record_for_inserting = (name, pw_hashed, email)
    sql = "Insert into user (username, password, email) values (%s, %s, %s)"
    # print(record_for_inserting)
    pointer.execute(sql, record_for_inserting)
    conn.commit()
    print ("Record inserted successfully into db")
    msg = Message('Your account info', sender='accrac016@gmail.com', recipients=['thainq00@gmail.com'])
    msg.body = "username: " + name + " pass: " + pw
    mail.send(msg)

    return jsonify({'code': 200, 'message': "create account successfully"})


@app.route('/login', methods=['POST'])
def login():
    # get body info
    req = request.get_json()
    name = req["username"]
    pw = req["password"]
    # check db
    pointer.execute("Select * from user where username = %s", name)
    print(pointer.fetchall())
    return jsonify({'stt': 200, 'data': { "name" : name}})


@app.route('/test', methods=['POST'])
def test():
    req = request.get_json()
    name = req["username"]
    pointer.execute("select id from user where username = %s", str(name))
    print(len(pointer.fetchall()))
    return jsonify({'stt' : 200, 'data': { "auth": 'true'}})