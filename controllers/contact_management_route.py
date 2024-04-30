from flask import Blueprint, request, jsonify
from models.contact_model import Contact
from utils.db import db
from sqlalchemy.exc import SQLAlchemyError

contact_routes = Blueprint('contact_routes', __name__)

# Get all contacts
@contact_routes.route('/contacts', methods=["GET"])
def get_contacts():
    try:
        contacts = Contact.query.all()
        contacts_data = [contact.to_dict() for contact in contacts]
        return jsonify(contacts_data)
    except SQLAlchemyError as e:
        return jsonify({'error': 'Gagal mengambil data kontak', 'message': str(e)}), 500

# Add a new contact
@contact_routes.route('/contacts', methods=["POST"])
def add_contact():
    data = request.get_json()
    try:
        new_contact = Contact(name=data['name'], email=data['email'], messages=data.get('messages'))
        db.session.add(new_contact)
        db.session.commit()
        return jsonify({'message': 'Kontak berhasil ditambahkan'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Gagal menambahkan kontak', 'error': str(e)}), 500

# Update a contact
@contact_routes.route('/contacts/<int:contact_id>', methods=["PUT"])
def update_contact(contact_id):
    data = request.get_json()
    try:
        contact = Contact.query.filter_by(id=contact_id).first()
        if not contact:
            return jsonify({'message': 'Kontak tidak ditemukan'}), 404
        contact.name = data.get('name', contact.name)
        contact.email = data.get('email', contact.email)
        contact.messages = data.get('messages', contact.messages)
        db.session.commit()
        return jsonify({'message': 'Kontak berhasil diperbarui'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Gagal memperbarui kontak', 'error': str(e)}), 500

# Delete a contact
@contact_routes.route('/contacts/<int:contact_id>', methods=["DELETE"])
def delete_contact(contact_id):
    try:
        contact = Contact.query.filter_by(id=contact_id).first()
        if not contact:
            return jsonify({'message': 'Kontak tidak ditemukan'}), 404
        db.session.delete(contact)
        db.session.commit()
        return jsonify({'message': 'Kontak berhasil dihapus'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Gagal menghapus kontak', 'error': str(e)}), 500
