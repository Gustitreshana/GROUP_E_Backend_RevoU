from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session, sessionmaker
import os

# Creating a SQLAlchemy db object without direct initialization
db = SQLAlchemy()

name = os.getenv('DB_NAME')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')

DATABASE_URI = f'mysql+pymysql://{user}:{password}@{host}:{port}/{name}'
engine = create_engine(DATABASE_URI)
Session = scoped_session(sessionmaker(bind=engine))

def init_db(app):
    try:
        db.init_app(app)
        with app.app_context():
            db.create_all()
            print(f'Successfully connected to the database at {host}')
    except SQLAlchemyError as e:
        print(f'Error connecting to the database: {e}')
