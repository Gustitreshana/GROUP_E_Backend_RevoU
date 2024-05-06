from flask import Blueprint, request, jsonify
from models.profile_model import Profile
from models.user_model import User
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from utils.db import db

profile_routes = Blueprint('profile_routes', __name__)

@profile_routes.route('/profiles', methods=["GET"])
@jwt_required()
def get_profiles():
    try:
        profiles = Profile.query.all()
        profiles_data = [profile.to_dict() for profile in profiles]
        return jsonify(profiles_data)
    except SQLAlchemyError as e:
        return jsonify({'error': 'Failed to fetch profiles', 'message': str(e)}), 500

@profile_routes.route('/profiles', methods=["POST"])
@jwt_required()
def create_profile():
    data = request.get_json()
    try:
        new_profile = Profile(
            realname=data['realname'],
            address=data['address'],
            occupation=data['occupation'],
            user_id=data['user_id']
        )
        db.session.add(new_profile)
        db.session.commit()
        return jsonify({'message': 'Profile successfully added'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to add profile', 'error': str(e)}), 500

@profile_routes.route('/admin/profiles/<int:profile_id>', methods=["PUT"])
@jwt_required()
def update_profile(profile_id):
    data = request.get_json()
    try:
        profile = Profile.query.filter_by(id=profile_id).first()
        if not profile:
            return jsonify({'message': 'Profile not found'}), 404
        
        profile.realname = data.get('realname', profile.realname)
        profile.address = data.get('address', profile.address)
        profile.occupation = data.get('occupation', profile.occupation)
        db.session.commit()
        return jsonify({'message': 'Profile successfully updated'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update profile', 'error': str(e)}), 500
    
@profile_routes.route('/admin/profiles/<int:profile_id>', methods=["DELETE"])
@jwt_required()
def delete_profile(profile_id):
    try:
        profile = Profile.query.filter_by(id=profile_id).first()
        if not profile:
            return jsonify({'message': 'Profile not found'}), 404
        
        db.session.delete(profile)
        db.session.commit()
        return jsonify({'message': 'Profile successfully deleted'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to delete profile', 'error': str(e)}), 500
