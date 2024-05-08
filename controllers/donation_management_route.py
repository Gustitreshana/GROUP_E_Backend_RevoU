from flask import Blueprint, request, jsonify
from models.donation_model import Donation
from models.user_model import User
from utils.db import db
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from utils.rupiah_format import format_rupiah
from flask_jwt_extended import get_jwt_identity

donation_routes = Blueprint('donation_routes', __name__)

# Create a donation
@donation_routes.route('/donations', methods=['POST'])
@jwt_required()
def create_donation():
    data = request.get_json()
    try:
        new_donation = Donation(
            nominal=data['nominal'],
            from_id=data['from_id']
        )
        db.session.add(new_donation)
        db.session.commit()
        return jsonify({'message': 'Donation successfully added', 'donation_id': new_donation.id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to add donation', 'error': str(e)}), 500

# Create a donation based on current user ID
@donation_routes.route('/donations/current-user', methods=['POST'])
@jwt_required()
def create_donation_auto():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    try:
        new_donation = Donation(
            nominal=data['nominal'],
            from_id=current_user_id
        )
        db.session.add(new_donation)
        db.session.commit()
        return jsonify({'message': 'Donation successfully added', 'donation_id': new_donation.id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to add donation', 'error': str(e)}), 500

# Get all donations
@donation_routes.route('/donations/user/data', methods=['GET'])
@jwt_required()
def get_donations():
    try:
        donations = Donation.query.join(User).all()
        donations_list = [{
            'id': donation.id,
            'nominal': format_rupiah(donation.nominal),
            'donor_name': donation.donor.realname,
            'created_at': donation.created_at
        } for donation in donations]
        return jsonify({'message': 'Donations retrieved successfully', 'donations': donations_list}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve donations', 'error': str(e)}), 500

# Update a donation
@donation_routes.route('/donations/user/admin/<int:donation_id>', methods=['PUT'])
@jwt_required()
def update_donation(donation_id):
    data = request.get_json()
    try:
        donation = Donation.query.filter_by(id=donation_id).first()
        if donation:
            donation.nominal = data.get('nominal', donation.nominal)
            db.session.commit()
            return jsonify({'message': 'Donation updated successfully'}), 200
        else:
            return jsonify({'message': 'Donation not found'}), 404
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update donation', 'error': str(e)}), 500

# Delete a donation
@donation_routes.route('/donations/user/admin/<int:donation_id>', methods=['DELETE'])
@jwt_required()
def delete_donation(donation_id):
    try:
        donation = Donation.query.filter_by(id=donation_id).first()
        if donation:
            db.session.delete(donation)
            db.session.commit()
            return jsonify({'message': 'Donation deleted successfully'}), 200
        else:
            return jsonify({'message': 'Donation not found'}), 404
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to delete donation', 'error': str(e)}), 500
