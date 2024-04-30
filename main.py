from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from utils.db import init_db
from controllers.user_management_route import user_routes
from controllers.contact_management_route import contact_routes

# Initializing Flask application
app = Flask(__name__)

# Setting database URI directly
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:tMvaPMeZxjeNENRLoYltgzgqtAslgdDa@monorail.proxy.rlwy.net:11463/zero_hunger"

# Initializing database
init_db(app)

# Setting JWT secret key directly
app.config['JWT_SECRET_KEY'] = "CQbWLxP5s6Wah6NWHz6ElSMxpbJnVD6BTX2CimbnzfyKQU7dNfDLGg8k6eMVJ1h8AY0hQu3fCpK9YvTFzwNfIsHCZ_ckUm-WPmre4t0KEwqx577w8WPvl_IKjfof5qJDJgJthdcL6cBDb5x-CRGoArjA60ukIKeO-S2v7suOmg6YPllB1PWzK89r0jyJT9vxiX6ANcwOJEIijrQpLpFSdyGeHvHx3_ulbQjtzLrOZdImCW6FAhtYGBBQyteMeofXpoUgDGhFOJv2cHt9_ILhvCAo1iNLlZ3HobQUGnpl-wYlrUWWiNsdFTi2cPBW-Oo6Ys-jP-FCfkAFJTnFLCkRfw"

# Registering blueprints
app.register_blueprint(user_routes)
app.register_blueprint(contact_routes)

# Defining routes here
@app.route('/')
def home():
    return jsonify({"message": "Hello, Zero Hunger API!"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
