from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from app.models.user_model import User
from app.utils.db import db
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import SQLAlchemyError

user_routes = Blueprint('user_routes', __name__)
bcrypt = Bcrypt()

# Registration Page
@user_routes.route('/register', methods=["GET"])
def register_page():
    try:
        # Querying to get all users
        users = User.query.all()
        
        # Converting user data to JSON format
        users_data = []
        for user in users:
            user_data = {
                'id': user.id,
                'name': user.username,
                'email': user.email,
                'created_at': user.created_at,
                'updated_at': user.updated_at
            }
            users_data.append(user_data)
        
        # Returning user data as JSON
        return jsonify(users_data)
    except SQLAlchemyError as e:
        # Returning an error message if there is a database query error
        return jsonify({'error': 'Failed to fetch user data', 'message': str(e)}), 500

# Registering a new user
@user_routes.route('/register', methods=["POST"])
def create_user():
    # Retrieving data from the request
    data = request.get_json()

    try:
        # Checking if the user already exists
        user_exists = User.query.filter_by(email=data['email']).first()
        if user_exists:
            return jsonify({'message': 'User already registered'}), 400

        # Encrypting password with bcrypt
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        # Creating a new user
        new_user = User(username=data['username'], email=data['email'], password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User successfully added'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to add user', 'error': str(e)}), 500
    
@user_routes.route('/register', methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    try:
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        # Update password if provided
        if 'password' in data:
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            user.password_hash = hashed_password
        db.session.commit()
        return jsonify({'message': 'User successfully updated'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update user', 'error': str(e)}), 500

@user_routes.route('/register', methods=["DELETE"])
def delete_user(user_id):
    try:
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User successfully deleted'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to delete user', 'error': str(e)}), 500

# Login Page
@user_routes.route('/login', methods=["POST"])
def login_user():
    data = request.get_json()

    try:
        # Checking if the user is registered
        user = User.query.filter_by(email=data['email']).first()
        if user and bcrypt.check_password_hash(user.password_hash, data['password']):
            # Creating JWT token
            access_token = create_access_token(identity=user.id)
            return jsonify({'message': 'Login successful', 'access_token': access_token}), 200
        else:
            return jsonify({'message': 'Incorrect email or password'}), 401
    except Exception as e:
        return jsonify({'message': 'Failed during login', 'error': str(e)}), 500
