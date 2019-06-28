import pytest
from flask import json
import main

from TekoTrainingModule.helpers import message
from TekoTrainingModule import app as App


@pytest.fixture
def app():
    app = App
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
    assert res.get_json().get('message') == message.ACOUNT_EXIST


def test_register_1(app):
    res = app.post('/register',
                   data=json.dumps({"username": "1abccc", "password": "1234", "email": "thainq00@gmail.com"}),
                   content_type='application/json')
    assert res.status_code == 400
    assert res.get_json().get('message') == message.EMAIL_EXIST


# def test_register_2(app):
#     app.post('/delete_for_testing',
#              data=json.dumps({"username": "thainq03"}),
#              content_type='application/json')
#     res = app.post('/register',
#                    data=json.dumps({"username": "thainq03", "password": "1234", "email": "thainq03@gmail.com"}),
#                    content_type='application/json')
#     assert res.status_code == 200
#     assert res.get_json().get('message') == message.CREATE_ACCOUNT


def test_login(app):
    res = app.post(
        '/login',
        data=json.dumps({"username": "thainq00", "password": "1"}),
        content_type='application/json'
    )
    data = res.get_json()
    assert res.status_code == 200
    assert data.get('code') == 200
    assert data.get('message') == message.LOGIN_SUCCESS


def test_login_2(app):
    res = app.post(
        '/login',
        data=json.dumps({"username": "thainq01", "password": "123456"}),
        content_type='application/json'
    )
    data = res.get_json()
    assert res.status_code == 400
    assert data.get('message') == message.WRONG_PASSWORD


def test_login_3(app):
    res = app.post(
        '/login',
        data=json.dumps({"password": "123456"}),
        content_type='application/json'
    )
    data = res.get_json()
    assert res.status_code == 400
    assert data.get('message') == message.USERNAME_PASSWORD_REQUIRED


def test_login_4(app):
    res = app.post(
        '/login',
        data=json.dumps({"username": "thainq01"}),
        content_type='application/json'
    )
    data = res.get_json()
    assert res.status_code == 400
    assert data.get('message') == message.USERNAME_PASSWORD_REQUIRED


def test_login_5(app):
    res = app.post(
        '/login',
        data=json.dumps({}),
        content_type='application/json'
    )
    data = res.get_json()
    assert res.status_code == 400
    assert data.get('message') == message.USERNAME_PASSWORD_REQUIRED


# def test_forgotPass_1(app):
#     res = app.post(
#         '/forgotPass',
#         data=json.dumps({"username": "thainq01", "email": "accrac020@gmail.com"}),
#         content_type='application/json'
#     )
#     assert res.status_code == 200
#     assert res.get_json().get('message') == message.SEND_NEW_PASS


def test_forgotPass_2(app):
    res = app.post(
        '/forgotPass',
        data=json.dumps({"username": "thainq02", "email": "accrac020@gmail.com"}),
        content_type='application/json'
    )
    assert res.status_code == 400
    assert res.get_json().get('message') == message.USERNAME_EMAIL_WRONG


def test_forgotPass_3(app):
    res = app.post(
        '/forgotPass',
        data=json.dumps({"username": "thainq0x", "email": "accrac020@gmail.com"}),
        content_type='application/json'
    )
    assert res.status_code == 404
    assert res.get_json().get('message') == message.USERNAME_NOT_FOUND


def test_forgotPass_4(app):
    res = app.post(
        '/forgotPass',
        data=json.dumps({"username": "thainq02"}),
        content_type='application/json'
    )
    assert res.status_code == 400
    assert res.get_json().get('message') == message.EMAIL_REQUIRED


def test_forgotPass_5(app):
    res = app.post(
        '/forgotPass',
        data=json.dumps({"email": "accrac020@gmail.com"}),
        content_type='application/json'
    )
    assert res.status_code == 400
    assert res.get_json().get('message') == message.USERNAME_REQUIRED

def test_forgotPass_6(app):
    res = app.post(
        '/forgotPass',
        data=json.dumps({}),
        content_type='application/json'
    )
    assert res.status_code == 400
    assert res.get_json().get('message') == message.ALL_FIELDS_REQUIRED


# def test_changePass_1(app):
#     res = app.post(
#         '/changePass',
#         data=json.dumps({"username": "thainq00", "password": "1", "newpassword": "2"}),
#         content_type='application/json'
#     )
#     assert res.status_code == 200
#     assert res.get_json().get('message') == message.CHANGE_PASSWORD_SUCCESS


def test_changePass_2(app):
    res = app.post(
        '/changePass',
        data=json.dumps({"password": "1", "newpassword": "2"}),
        content_type='application/json'
    )
    assert res.status_code == 400
    assert res.get_json().get('message') == message.USERNAME_REQUIRED


def test_changePass_3(app):
    res = app.post(
        '/changePass',
        data=json.dumps({"username": "thainq00", "newpassword": "2"}),
        content_type='application/json'
    )
    assert res.status_code == 400
    assert res.get_json().get('message') == message.PASSWORD_REQUIRED


def test_changePass_4(app):
    res = app.post(
        '/changePass',
        data=json.dumps({"username": "thainq00", "password": "1"}),
        content_type='application/json'
    )
    assert res.status_code == 400
    assert res.get_json().get('message') == message.NEW_PASSWORD_REQUIRED


def test_changePass_5(app):
    res = app.post(
        '/changePass',
        data=json.dumps({"username": "thainq00", "password": "11", "newpassword": "2"}),
        content_type='application/json'
    )
    assert res.status_code == 400
    assert res.get_json().get('message') == message.WRONG_USERNAME_PASSWORD


def test_changePass_6(app):
    res = app.post(
        '/changePass',
        data=json.dumps({"username": "thainq00", "password": "1", "newpassword": "1"}),
        content_type='application/json'
    )
    assert res.status_code == 400
    assert res.get_json().get('message') == message.OLD_NEW_PASSWORD_DIFFERENT
