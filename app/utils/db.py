from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session, sessionmaker
import os

# Creating a SQLAlchemy db object without direct initialization
db = SQLAlchemy()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DATABASE_URI = os.getenv('DATABASE_URI')

engine = create_engine(DATABASE_URI)
Session = scoped_session(sessionmaker(bind=engine))

def init_db(app):
    try:
        db.init_app(app)
        with app.app_context():
            db.create_all()
            print(f'Successfully connected to the database using provided URI')
    except SQLAlchemyError as e:
        print(f'Error connecting to the database: {e}')
