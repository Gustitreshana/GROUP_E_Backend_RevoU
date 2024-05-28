
from flask import Blueprint, jsonify, request
from sqlalchemy.sql import func
from app.models.donasi import Donasi
from app.models.donatur import Donatur
from app.models.program import Program
from app.models.user import User
from app.utils.db import db
from app.service.donasi_service import Donasi_service
from app.utils.api_response import api_response
from flask_jwt_extended import jwt_required, get_jwt_identity

donasi_blueprint = Blueprint('donasi_endpoint', __name__)

@donasi_blueprint.route('/', methods=['POST'])
@jwt_required()
def create_donasi():
    try:
        data = request.get_json()
        
        # Pastikan data yang diperlukan ada
        required_fields = ['pesan_doa', 'rupiah', 'tipe_pembayaran', 'donatur_id', 'program_id']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'{field} harus disertakan'}), 400
        
        # Cek tipe data untuk 'rupiah'
        if not isinstance(data['rupiah'], (int, float)):
            return jsonify({'message': 'Jumlah donasi harus berupa angka'}), 400

        # Mendapatkan identitas pengguna dari token JWT
        current_user_id = get_jwt_identity()

        # Cek apakah user yang sedang login sesuai dengan donatur_id yang diberikan
        donatur = Donatur.query.filter_by(donatur_id=data['donatur_id'], user_id=current_user_id).first()
        if not donatur:
            return jsonify({'message': 'Anda tidak diizinkan membuat donasi untuk donatur lain atau donatur tidak ditemukan'}), 403
        
        # Cek apakah program_id sesuai dengan program yang dimiliki user yang sedang login
        program = Program.query.filter_by(program_id=data['program_id'], user_id=current_user_id).first()
        if not program:
            return jsonify({'message': 'Program tidak ditemukan atau Anda tidak memiliki izin untuk program ini'}), 403

        # Membuat objek DTO sederhana
        donasi_data_dto = type('DonasiDTO', (object,), data)

        # Menggunakan service untuk membuat donasi
        donasi_service = Donasi_service()
        created_donasi = donasi_service.create_donasi(donasi_data_dto, current_user_id, data['donatur_id'], data['program_id'])

        return api_response(
            status_code=201,
            message="success input data donasimu.. terima kash",
            data=created_donasi
        )
    
    except Exception as e:
        # Tangani kesalahan server jika ada
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )

@donasi_blueprint.route('/list_donasiku', methods=['GET'])
@jwt_required()  # Membutuhkan token JWT untuk akses
def get_donasiku():
    try:

        # Mendapatkan identitas pengguna yang saat ini login dari token JWT
        current_user_id = get_jwt_identity()

        # Querying untuk mendapatkan data pengguna yang saat ini login
        user = User.query.filter_by(id=current_user_id).first()

        # Memastikan pengguna ditemukan
        if not user:
            return api_response(
                status_code=404,
                message="User not found",
                data={}
            )

        # Mendapatkan data donatur yang terkait dengan user
        donasis = Donasi.query.filter_by(user_id=current_user_id).all()

        donasis_data = [{
            'donasi_id': donasi.donasi_id,
            'user_id': donasi.user_id,
            'donatur_id': donasi.donatur_id,
            'program_id': donasi.program_id,
            'rupiah' : donasi.rupiah,
            'donasi_datetime': donasi.donasi_datetime
            
        } for donasi in donasis]

        return api_response(
            status_code=200,
            message="Daftar donasi anda sukses diakses",
            data=donasis_data
        )  
    except Exception as e:
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )       
