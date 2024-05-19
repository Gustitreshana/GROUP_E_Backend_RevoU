from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from app.utils.db import db
from app.controllers.user import user_route
# from app.controllers.contact_management_route import contact_routes
# from app.controllers.donation_management_route import donation_routes
from app.controllers.program import program_route
from app.controllers.donatur import donatur_route
from app.controllers.donasi import donasi_route
from dotenv import load_dotenv
from flask_cors import CORS
import os

# Initializing Flask application
app = Flask(__name__)

CORS(app)

load_dotenv()

# Setting database URI directly
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

# Initializing database
db.init_app(app)

# Setting JWT secret key directly
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

# Registering blueprints
app.register_blueprint(user_route.user_blueprint, url_prefix='/user')
app.register_blueprint(program_route.program_blueprint, url_prefix='/programs')
app.register_blueprint(donatur_route.donatur_blueprint, url_prefix='/programs/donatur')
app.register_blueprint(donasi_route.donasi_blueprint, url_prefix='/programs/donasi')

# Defining routes here
@app.route('/')
def index():
    return jsonify({'message': 'Sukses..sukses..sukess !!!'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)