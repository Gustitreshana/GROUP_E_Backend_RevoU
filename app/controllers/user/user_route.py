from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from app.models.user import User, db
from app.utils.api_response import api_response
from app.utils.db import db
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from sqlalchemy.exc import SQLAlchemyError

from werkzeug.security import generate_password_hash
import bcrypt
import re

user_blueprint = Blueprint('user_endpoint', __name__)
bcrypt = Bcrypt()

# Registration Page
@user_blueprint.route('/all', methods=["GET"])
def all_register():
    try:
        # Querying to get all users
        users = User.query.all()
        
        # Converting user data to JSON format
        users_data = []
        for user in users:
            user_data = {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'password': user.password,
                'role': user.role,
                'created_at': user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                'updated_at': user.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            }
            users_data.append(user_data)
        
        # Returning user data as JSON
        return jsonify(users_data)
    except SQLAlchemyError as e:
        # Returning an error message if there is a database query error
        return jsonify({'error': 'Failed to fetch user data', 'message': str(e)}), 500

@user_blueprint.route('/', methods=["GET"])
@jwt_required()  # Membutuhkan token JWT untuk akses
def user_register():
    try:
        # Mendapatkan identitas pengguna yang saat ini login dari token JWT
        current_user_id = get_jwt_identity()

        # Querying untuk mendapatkan data pengguna yang saat ini login
        user = User.query.filter_by(id=current_user_id).first()

        # Memastikan pengguna ditemukan
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Mengonversi data pengguna ke format JSON
        user_data = {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'password': user.password,
                'role': user.role,
                'created_at': user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                'updated_at': user.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }

        # Mengembalikan data pengguna sebagai JSON
        return jsonify(user_data)
    except SQLAlchemyError as e:
        # Mengembalikan pesan kesalahan jika ada kesalahan kueri basis data
        return jsonify({'error': 'Failed to fetch user data', 'message': str(e)}), 500

@user_blueprint.route('/all/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if user:
            return api_response(
                status_code=200,
                message="Daftar data dari id karyawan berhasil ditampilkan",
                data=[user.serialize()]
            )  
        else:
            return api_response(
                status_code=400,
                message="Data karyawan tidak ditemukan",
                data={}
            )  
    except Exception as e:
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        ) 
    
@user_blueprint.route('/edit', methods=["PUT"])
@jwt_required()  # Membutuhkan token JWT untuk akses
def update_profile():
    try:
        # Mendapatkan identitas pengguna yang saat ini login dari token JWT
        current_user_id = get_jwt_identity()

        # Mendapatkan data pengguna yang saat ini login
        user = User.query.filter_by(id=current_user_id).first()

        # Memastikan pengguna ditemukan
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Mendapatkan data yang akan diubah dari permintaan
        data = request.json

        # Memperbarui data pengguna
        user.email = data.get('email', user.email)
        user.name = data.get('name', user.name)
        # user.role = data.get('role', user.role)

        # Commit perubahan ke database
        db.session.commit()

        # Mengembalikan pesan sukses
        return jsonify({'message': 'data user updated successfully'}), 200
    except SQLAlchemyError as e:
        # Mengembalikan pesan kesalahan jika ada kesalahan kueri basis data
        return jsonify({'error': 'Failed to update profile', 'message': str(e)}), 500


# Registering a new user
@user_blueprint.route('/register', methods=["POST"])
def create_user():
    data = request.get_json()

    # Validate input data
    if not data or not 'email' in data or not 'name' in data or not 'password' in data:
        return jsonify({'message': 'Missing required fields'}), 400

    email = data['email']
    name = data['name']
    password = data['password']

    # Email format validation
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        return jsonify({'message': 'Invalid email format'}), 400

    # Password complexity validation
    if len(password) < 8:
        return jsonify({'message': 'Password must be at least 8 characters long'}), 400

    try:
        # Checking if the user already exists
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            return jsonify({'message': 'User already registered'}), 400

        # Encrypting password with bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Creating a new user
        new_user = User(
            email=email,
            name=name,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User successfully added'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to add user', 'error': str(e)}), 500
    
@user_blueprint.route('/admin/all/<int:user_id>', methods=["PUT"])
@jwt_required() 
def update_user(user_id):
    data = request.get_json()
    try:
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        user.email = data.get('email', user.email)
        user.name = data.get('name', user.name)
        # Update password if provided
        if 'password' in data:
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            user.password_hash = hashed_password
        db.session.commit()
        return jsonify({'message': 'User successfully updated'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update user', 'error': str(e)}), 500

@user_blueprint.route('/admin/all/<int:user_id>', methods=["DELETE"])
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

# Login Page
@user_blueprint.route('/login', methods=["POST"])
def login_user():
    data = request.get_json()

    try:
        # Checking if the user is registered
        user = User.query.filter_by(email=data['email']).first()
        if user and bcrypt.check_password_hash(user.password, data['password']):
            # Creating JWT token
            access_token = create_access_token(identity=user.id)
            return jsonify({'message': 'Login successful', 'access_token': access_token}), 200
        else:
            return jsonify({'message': 'Incorrect email or password'}), 401
    except Exception as e:
        return jsonify({'message': 'Failed during login', 'error': str(e)}), 500
