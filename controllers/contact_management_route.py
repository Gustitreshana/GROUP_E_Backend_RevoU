from flask import Blueprint, request, jsonify
from models.contact_model import Contact
from utils.db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

contact_routes = Blueprint('contact_routes', __name__)

# Get all contacts
@contact_routes.route('/contacts/user/data', methods=["GET"])
@jwt_required()
def get_contacts():
    try:
        contacts = Contact.query.all()
        contacts_data = [contact.to_dict() for contact in contacts]
        return jsonify(contacts_data)
    except SQLAlchemyError as e:
        return jsonify({'error': 'Failed to fetch contact data', 'message': str(e)}), 500

# Add a new contact
@contact_routes.route('/contacts/user', methods=["POST"])
@jwt_required()
def add_contact():
    data = request.get_json()
    try:
        new_contact = Contact(name=data['name'], email=data['email'], messages=data.get('messages'))
        db.session.add(new_contact)
        db.session.commit()
        return jsonify({'message': 'Contact successfully added'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to add contact', 'error': str(e)}), 500

# Update a contact
@contact_routes.route('/contacts/user/admin/<int:contact_id>', methods=["PUT"])
@jwt_required()
def update_contact(contact_id):
    data = request.get_json()
    try:
        contact = Contact.query.filter_by(id=contact_id).first()
        if not contact:
            return jsonify({'message': 'Contact not found'}), 404
        contact.name = data.get('name', contact.name)
        contact.email = data.get('email', contact.email)
        contact.messages = data.get('messages', contact.messages)
        db.session.commit()
        return jsonify({'message': 'Contact successfully updated'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update contact', 'error': str(e)}), 500

# Delete a contact
@contact_routes.route('/contacts/user/admin/<int:contact_id>', methods=["DELETE"])
@jwt_required()
def delete_contact(contact_id):
    try:
        contact = Contact.query.filter_by(id=contact_id).first()
        if not contact:
            return jsonify({'message': 'Contact not found'}), 404
        db.session.delete(contact)
        db.session.commit()
        return jsonify({'message': 'Contact successfully deleted'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to delete contact', 'error': str(e)}), 500
