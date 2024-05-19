from flask import Blueprint, jsonify, request
from sqlalchemy import func
from app.models.donasi import Donasi
from app.utils.db import db

donasi_blueprint = Blueprint('donasi_endpoint', __name__)

@donasi_blueprint.route('/', methods=['POST'])
def add_donation():
    try:
        data = request.get_json()
        # Pastikan data yang diperlukan ada dan sesuai dengan skema yang diharapkan
        if 'rupiah' not in data:
            return jsonify({'message': 'Jumlah donasi harus disertakan'}), 400
        # Anda juga dapat memeriksa tipe data jika diperlukan
        if not isinstance(data['rupiah'], (int, float)):
            return jsonify({'message': 'Jumlah donasi harus berupa angka'}), 400
        
        # Buat objek Donasi baru
        new_donation = Donasi(
            pesan_doa=data['pesan_doa'],
            rupiah=data['rupiah'],
            tipe_pembayaran = data['tipe_pembayaran'],
            donasi_datetime = func.now()
        )
        db.session.add(new_donation)
        db.session.commit()
        
        return jsonify({'message': 'Donasi berhasil ditambahkan'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Gagal menambahkan donasi', 'error': str(e)}), 500
