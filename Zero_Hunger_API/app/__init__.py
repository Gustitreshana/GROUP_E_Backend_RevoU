from flask import Flask
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from app.utils.db import init_db
from app.controllers.user_management_route import user_routes
from app.controllers.contact_management_route import contact_routes
import os

# Memuat variabel lingkungan
load_dotenv()

# Menginisialisasi aplikasi Flask
def create_app():
    app = Flask(__name__)

    # Mengatur URI database dari file .env
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')

    # Menginisialisasi database
    init_db(app)

    # Mengatur kunci rahasia JWT dari file .env
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    JWTManager(app)
    
    # Mendaftarkan blueprint
    app.register_blueprint(user_routes)
    app.register_blueprint(contact_routes)

    # Mendefinisikan route di sini
    @app.route('/')
    def home():
        return "Halo, Dunia!"

    return app
