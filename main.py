from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from utils.db import init_db
from controllers.user_management_route import user_routes
from controllers.contact_management_route import contact_routes
from dotenv import load_dotenv
import os

# Initializing Flask application
app = Flask(__name__)

load_dotenv()

# Setting database URI directly
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

# Initializing database
init_db(app)

# Setting JWT secret key directly
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

# Registering blueprints
app.register_blueprint(user_routes)
app.register_blueprint(contact_routes)

# Defining routes here
@app.route('/')
def home():
    return jsonify({"message": "Hello, Zero Hunger API!"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
