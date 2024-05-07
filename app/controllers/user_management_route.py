from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from models.user_model import User
from app.utils.api_response import api_response
from utils.db import db
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
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
                'realname': user.realname,
                'address': user.address,
                'occupation': user.occupation,
                'created_at': user.created_at,
                'updated_at': user.updated_at
            }
            users_data.append(user_data)
        
        # Returning user data as JSON
        return jsonify(users_data)
    except SQLAlchemyError as e:
        # Returning an error message if there is a database query error
        return jsonify({'error': 'Failed to fetch user data', 'message': str(e)}), 500

@user_routes.route('/users', methods=["GET"])
@jwt_required()  # Membutuhkan token JWT untuk akses
def register_page():
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
            'name': user.username,
            'email': user.email,
            'realname': user.realname,
            'address': user.address,
            'occupation': user.occupation,
            'created_at': user.created_at,
            'updated_at': user.updated_at
        }

        # Mengembalikan data pengguna sebagai JSON
        return jsonify(user_data)
    except SQLAlchemyError as e:
        # Mengembalikan pesan kesalahan jika ada kesalahan kueri basis data
        return jsonify({'error': 'Failed to fetch user data', 'message': str(e)}), 500

@user_routes.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if user:
            return api_response(
                status_code=200,
                message="Daftar data dari id karyawan berhasil ditampilkan",
                data=[user.as_dict()]
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
    
from flask_jwt_extended import jwt_required, get_jwt_identity

@user_routes.route('/profile', methods=["PUT"])
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
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.realname = data.get('realname', user.realname)
        user.address = data.get('address', user.address)
        user.occupation = data.get('occupation', user.occupation)

        # Commit perubahan ke database
        db.session.commit()

        # Mengembalikan pesan sukses
        return jsonify({'message': 'Profile updated successfully'}), 200
    except SQLAlchemyError as e:
        # Mengembalikan pesan kesalahan jika ada kesalahan kueri basis data
        return jsonify({'error': 'Failed to update profile', 'message': str(e)}), 500


# Registering a new user
@user_routes.route('/register', methods=["POST"])
def create_user():
    data = request.get_json()

    try:
        # Checking if the user already exists
        user_exists = User.query.filter_by(email=data['email']).first()
        if user_exists:
            return jsonify({'message': 'User already registered'}), 400

        # Encrypting password with bcrypt
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        # Creating a new user
        new_user = User(
            username=data['username'],
            email=data['email'],
            password_hash=hashed_password,
            realname=data.get('realname'),  # Menambahkan realname
            address=data.get('address'),    # Menambahkan address
            occupation=data.get('occupation')  # Menambahkan occupation
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User successfully added'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to add user', 'error': str(e)}), 500
    
@user_routes.route('/admin/user/<int:user_id>', methods=["PUT"])
@jwt_required() 
def update_user(user_id):
    data = request.get_json()
    try:
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.realname = data.get('realname', user.realname)  # Memperbarui realname
        user.address = data.get('address', user.address)    # Memperbarui address
        user.occupation = data.get('occupation', user.occupation)  # Memperbarui occupation
        # Update password if provided
        if 'password' in data:
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            user.password_hash = hashed_password
        db.session.commit()
        return jsonify({'message': 'User successfully updated'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update user', 'error': str(e)}), 500

@user_routes.route('/admin/user/<int:user_id>', methods=["DELETE"])
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
