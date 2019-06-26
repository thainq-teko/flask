from sqlalchemy import create_engine

engine = create_engine('mysql://teko:1234@localhost:3306/flask_db?get-server-public-key=true')


def connectDB(app):
    return app.connect()
