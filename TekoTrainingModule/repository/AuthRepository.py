from TekoTrainingModule.model.User import User
from TekoTrainingModule.config import connectDB

session = connectDB.loadSession()


def get_all_user():
    res = session.query(User).all()
    return res


def get_id_by_username(name):
    res = session.query(User.id).filter_by(username=name).one_or_none()
    return res


def get_id_by_email(email):
    res = session.query(User.id).filter_by(username=email).one_or_none()
    return res


def add_user(username, email, password):
    new_user = User(username=username, email=email, password=password)
    session.add(new_user)
    session.commit()
    return 1


def get_user_by_username(username):
    res = session.query(User).filter_by(username=username).one_or_none()
    return res


def get_password_by_username(username):
    res = session.query(User.password).filter_by(username=username).one_or_none()
    return res


def get_email_by_username(username):
    res = session.query(User.email).filter_by(username=username).one_or_none()
    return res


# def change_pass(password, email):
#     session.query(User).filter(User.email == email).update()
