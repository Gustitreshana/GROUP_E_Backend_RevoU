from flask import Flask
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from app.utils.db import init_db
from app.controllers.user_management_route import user_routes
from app.controllers.contact_management_route import contact_routes
import os

# Loading environment variables
load_dotenv()

# Initializing Flask application
def create_app():
    app = Flask(__name__)

    # Setting database URI from .env file
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')

    # Initializing database
    init_db(app)

    # Setting JWT secret key from .env file
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    JWTManager(app)
    
    # Registering blueprints
    app.register_blueprint(user_routes)
    app.register_blueprint(contact_routes)

    # Defining routes here
    @app.route('/')
    def home():
        return "Hello, Zero Hunger API!"

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 11463))
    app.run(host='0.0.0.0', port=port)