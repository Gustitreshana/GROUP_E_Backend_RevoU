from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from models.user_model import User
from utils.db import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

user_routes = Blueprint('user_routes', __name__)
bcrypt = Bcrypt()

# Get all users
@user_routes.route('/register/user/data', methods=["GET"])
def register_page():
    try:
        users = User.query.all()
        
        users_data = []
        for user in users:
            user_data = {
                'id': user.id,
                'name': user.username,
                'email': user.email,
                'realname': user.realname,
                'address': user.address,
                'occupation': user.occupation,
                'created_at': user.created_at,
                'updated_at': user.updated_at
            }
            users_data.append(user_data)
        
        return jsonify(users_data)
    except SQLAlchemyError as e:
        return jsonify({'error': 'Failed to fetch user data', 'message': str(e)}), 500

# Get current user
@user_routes.route('/current-user/data', methods=["GET"])
@jwt_required()
def get_current_user():
    try:
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        user_data = {
            'id': user.id,
            'name': user.username,
            'email': user.email,
            'realname': user.realname,
            'address': user.address,
            'occupation': user.occupation,
            'created_at': user.created_at,
            'updated_at': user.updated_at
        }
        
        return jsonify(user_data)
    except SQLAlchemyError as e:
        return jsonify({'error': 'Failed to fetch user data', 'message': str(e)}), 500

# Get user by id
@user_routes.route('/data/user/<int:user_id>', methods=["GET"])
def get_user_by_id(user_id):
    try:
        user = User.query.filter_by(id=user_id).first()
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        user_data = {
            'id': user.id,
            'name': user.username,
            'email': user.email,
            'realname': user.realname,
            'address': user.address,
            'occupation': user.occupation,
            'created_at': user.created_at,
            'updated_at': user.updated_at
        }
        
        return jsonify(user_data)
    except SQLAlchemyError as e:
        return jsonify({'error': 'Failed to fetch user data', 'message': str(e)}), 500

# Registering a new user
@user_routes.route('/register/user', methods=["POST"])
def create_user():
    data = request.get_json()

    try:
        user_exists = User.query.filter_by(email=data['email']).first()
        if user_exists:
            return jsonify({'message': 'User already registered'}), 400
        
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        new_user = User(
            username=data['username'],
            email=data['email'],
            password_hash=hashed_password,
            realname=data.get('realname'),
            address=data.get('address'),
            occupation=data.get('occupation')
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User successfully added'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to add user', 'error': str(e)}), 500

# Update user
@user_routes.route('/update/user/admin<int:user_id>', methods=["PUT"])
@jwt_required()
def update_user(user_id):
    data = request.get_json()
    try:
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.realname = data.get('realname', user.realname)
        user.address = data.get('address', user.address)
        user.occupation = data.get('occupation', user.occupation)
        # Update password if provided
        if 'password' in data:
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            user.password_hash = hashed_password
        db.session.commit()
        return jsonify({'message': 'User successfully updated'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update user', 'error': str(e)}), 500

# Update current user
@user_routes.route('/update/current-user', methods=["PUT"])
@jwt_required()
def update_current_user():
    user_id = get_jwt_identity()
    data = request.get_json()
    try:
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        # Memperbarui data pengguna yang sedang login
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.realname = data.get('realname', user.realname)
        user.address = data.get('address', user.address)
        user.occupation = data.get('occupation', user.occupation)
        
        # Update password jika disediakan
        if 'password' in data:
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            user.password_hash = hashed_password
        
        db.session.commit()
        return jsonify({'message': 'User successfully updated'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update user', 'error': str(e)}), 500

# Delete user
@user_routes.route('/user/admin/<int:user_id>', methods=["DELETE"])
@jwt_required()
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

# Login user
@user_routes.route('/login/user', methods=["POST"])
def login_user():
    data = request.get_json()

    try:
        user = User.query.filter_by(email=data['email']).first()
        if user and bcrypt.check_password_hash(user.password_hash, data['password']):
            access_token = create_access_token(identity=user.id)
            return jsonify({'message': 'Login successful', 'access_token': access_token}), 200
        else:
            return jsonify({'message': 'Incorrect email or password'}), 401
    except Exception as e:
        return jsonify({'message': 'Failed during login', 'error': str(e)}), 500
