import pytest
from flask import json
import main

@pytest.fixture
def app():
    app = main.create_app()
    app.debug = True
    return app.test_client()


def test_get_home(app):
    res = app.get("/")
    assert res.status_code == 200
    assert "Hello, flask app works ! - Thainq" in res.data


def test_register(app):
    res = app.post('/register',
                   data=json.dumps({"username": "thainq00", "password": "1234", "email": "thainq00@gmail.com"}),
                   content_type='application/json')
    assert res.status_code == 400
    assert res.get_json().get('message') == "account existed!"


def test_register_1(app):
    res = app.post('/register',
                   data=json.dumps({"username": "abcc", "password": "1234", "email": "thainq00@gmail.com"}),
                   content_type='application/json')
    assert res.status_code == 400
    assert res.get_json().get('message') == "email existed!"


# def test_register_2(app):
#     app.post('/delete_for_testing',
#              data=json.dumps({"username": "thainq03"}),
#              content_type='application/json')
#     res = app.post('/register',
#                    data=json.dumps({"username": "thainq03", "password": "1234", "email": "thainq03@gmail.com"}),
#                    content_type='application/json')
#     assert res.status_code == 200
#     assert res.get_json().get('message') == "create account successfully"


def test_login(app):
    res = app.post(
        '/login',
        data=json.dumps({"username": "thainq00", "password": "1"}),
        content_type='application/json'
    )
    data = res.get_json()
    assert res.status_code == 200
    assert data.get('code') == 200
    assert data.get('message') == 'login success'


def test_login_2(app):
    res = app.post(
        '/login',
        data=json.dumps({"username": "thainq01", "password": "123456"}),
        content_type='application/json'
    )
    assert res.status_code == 400


def test_login_3(app):
    res = app.post(
        '/login',
        data=json.dumps({"password": "123456"}),
        content_type='application/json'
    )
    assert res.status_code == 400


def test_login_4(app):
    res = app.post(
        '/login',
        data=json.dumps({"username": "thainq01"}),
        content_type='application/json'
    )
    assert res.status_code == 400


def test_login_5(app):
    res = app.post(
        '/login',
        data=json.dumps({}),
        content_type='application/json'
    )
    assert res.status_code == 400


# def test_forgotPass_1(app):
#     res = app.post(
#         '/forgotPass',
#         data=json.dumps({"username": "thainq01", "email": "accrac020@gmail.com"}),
#         content_type='application/json'
#     )
#     assert res.status_code == 200


def test_forgotPass_2(app):
    res = app.post(
        '/forgotPass',
        data=json.dumps({"username": "thainq02", "email": "accrac020@gmail.com"}),
        content_type='application/json'
    )
    assert res.status_code == 400
    assert res.get_json().get('message') == "user and email not belong together!"


def test_forgotPass_3(app):
    res = app.post(
        '/forgotPass',
        data=json.dumps({"username": "thainq0x", "email": "accrac020@gmail.com"}),
        content_type='application/json'
    )
    assert res.status_code == 404
    assert res.get_json().get('message') == "username not found!"


def test_forgotPass_4(app):
    res = app.post(
        '/forgotPass',
        data=json.dumps({"username": "thainq02"}),
        content_type='application/json'
    )
    assert res.status_code == 400
    assert res.get_json().get('message') == "email required!"


def test_forgotPass_5(app):
    res = app.post(
        '/forgotPass',
        data=json.dumps({"email": "accrac020@gmail.com"}),
        content_type='application/json'
    )
    assert res.status_code == 400
    assert res.get_json().get('message') == "username required!"


def test_forgotPass_6(app):
    res = app.post(
        '/forgotPass',
        data=json.dumps({}),
        content_type='application/json'
    )
    assert res.status_code == 400
    assert res.get_json().get('message') == "All fields required!"
