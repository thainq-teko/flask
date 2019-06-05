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
                   data=json.dumps({"username": "abc", "password": "1234", "email": "thainq00@gmail.com"}),
                   content_type='application/json')
    assert res.status_code == 200


def test_login(app):
    res = app.post(
        '/login',
        data=json.dumps({"username": "thainq00", "password": "123456"}),
        content_type='application/json'
    )
    assert res.status_code == 200


def test_login_2(app):
    res = app.post(
        '/login',
        data=json.dumps({"username": "thainq01", "password": "123456"}),
        content_type='application/json'
    )
    assert res.status_code == 404


def test_login_3(app):
    res = app.post(
        '/login',
        data=json.dumps({"password": "123456"}),
        content_type='application/json'
    )
    assert res.status_code == 400
