import flask
from flask import Flask,request, jsonify
from flask_cors import CORS

from flaskext.mysql import MySQL


app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'tekoer_test_flask'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
pointer = conn.cursor()
pointer.execute("SELECT * FROM user")
data = pointer.fetchall()
result = []
for i in data :
    result.append({
        'id' : i[0],
        'name': i[1].encode('ascii','ignore')
    })
print(result)

@app.route('/allUser', methods=['GET'])
def all_user():
    return jsonify(result)

@app.route('/login', methods=['POST'])
def login():
    req = request.get_json()
    idd = req["id"]
    name = req["username"]
    pointer.execute("Select * from user where id = %s", idd)
    print(pointer.fetchall())
    return jsonify({'stt': 200, 'data': { "id" : idd , "name" : name}})

@app.route('/test')
def test():
    return "1"
