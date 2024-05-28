from flask import Blueprint, jsonify, request, json
from app.decorators.role_checker import role_required
from app.models.user import User  # Import model User
from app.models.program import Program
from app.service.program_service import Program_service
from app.utils.api_response import api_response
from app.controllers.program.schema.create_program_request import Create_program_request
from app.controllers.program.schema.update_program_request import Update_program_request
from pydantic import ValidationError
from flask_login import current_user  # Import fungsi current_user dari Flask-Login
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required


program_blueprint = Blueprint('program_endpoint', __name__)

@program_blueprint.route('/', methods=['POST'])
@jwt_required() 
def create_program():
    try:
        # Ambil data pelanggan dari permintaan POST
        data = request.json

        # Pastikan data yang diperlukan tersedia
        if 'nama_program' not in data or 'lokasi_program' not in data:
            return api_response(
                status_code=400,
                message="Data kurang lengkap",
                data={  "contoh inputan ":
                        {
                            "nama_program":"Donasi makanan bergizi dhuafa",
                            "lokasi_program": "Kabupaten Luwu, Sulawesi Selatan"
                        }                       
                }
            )  
        
        # Mendapatkan identitas pengguna yang saat ini login dari token JWT
        current_user_id = get_jwt_identity()

        # Querying untuk mendapatkan data pengguna yang saat ini login
        user = User.query.filter_by(id=current_user_id).first()

        create_program_request = Create_program_request(**data)

        program_service = Program_service()

        # Panggil metode create_program dengan data program dan user_id
        programs = program_service.create_program(create_program_request, user.id)

        return api_response(
            status_code=201,
            message="success input data",
            data=programs
        )
    
    except Exception as e:
        # Tangani kesalahan server jika ada
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )  


@program_blueprint.route('/programdonasiku', methods=["GET"])
@jwt_required()  # Membutuhkan token JWT untuk akses
def only_userlogin_program():
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
        
        # Mendapatkan data program yang terkait dengan user
        programs = user.programs  # Asumsi ada relasi many-to-many

        programs_data = [{
            'program_id': program.program_id,
            'user_id': program.user_id,
            'nama_program': program.nama_program,
            'lokasi_program': program.lokasi_program,
            'created_at': program.created_at,
            'updated_at': program.updated_at
        } for program in programs]
        
        # return programs
        return api_response(
            status_code = 200,
            message ="Daftar semua program donasi anda sukses diakses",
            data = programs_data
        )       
    
    except Exception as e:
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )  


# --->>>--ADMIN-ACCESS--->>>--ADMIN--ACCESS--->>>>
@program_blueprint.route('/admin/all', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_programs():
    try:
        
        # Mendapatkan identitas pengguna yang saat ini login dari token JWT
        current_user_id = get_jwt_identity()

        # # Querying untuk mendapatkan data pengguna yang saat ini login
        # user = User.query.filter_by(id=current_user_id).first()


        program_service = Program_service()

        programs = program_service.get_programs(current_user_id)
        
        # return programs
        return api_response(
            status_code = 200,
            message ="Daftar semua program donasi sukses diakses",
            data = programs
        )
        
    except ValueError as ve:
        return api_response(
            status_code=404,
            message=str(ve),
            data={}
        )
    
    except PermissionError as pe:
        return api_response(
            status_code=403,
            message=str(pe),
            data={}
        )

    except Exception as e:
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )
        
@program_blueprint.route('/admin/<int:program_id>', methods=['GET'])
def get_program(program_id):
    try:
        program = Program.query.get(program_id)
        if program:
            return api_response(
                status_code=200,
                message="Daftar data dari id karyawan berhasil ditampilkan",
                data=[program.serialize()]
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

@program_blueprint.route('/admin/<int:program_id>', methods=['PUT'])
def update_program(program_id):
    try:

        data = request.json
        update_program_request = Update_program_request(**data)
        print(update_program_request)

        program_service = Program_service()
        programs = program_service.update_program(program_id, update_program_request)

        return api_response(
            status_code=200,
            message="succes update program data",
            data=programs
        ) 
    
    except ValidationError as e:
        return api_response(
            status_code=400,
            message=e.errors(),
            data={}
        )     
    except Exception as e:
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )   

@program_blueprint.route('/admin/<int:program_id>', methods=['DELETE'])
def delete_program(program_id):
    try:
        employe_service = Program_service()
        program = employe_service.delete_program(program_id)
        if program == "Program not available":
            return api_response(
            status_code=404,
            message=program,
            data={}
        )
        return api_response(
            status_code=200,
            message="Data program donasi berhasil dihapus",
            data=program
        )    
        
    except Exception as e:
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        ) 
    
@program_blueprint.route('/admin/search', methods=['GET'])
def search_programs():
    try:
        request_data = request.args
        
        program_service = Program_service()
        programs = program_service.search_programs(request_data['name'])
        if programs:
        # return [animal.as_dict() for animal in animals], 200
            return api_response(
                status_code=200,
                message="Daftar data program donasi yang dicari sukses diakses",
                data=programs
            )  
        else:
            return api_response(
                status_code=400,
                message="Data program donasi yang dicari tidak ditemukan",
                data={}
            )   
    except Exception as e:
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )       

# -------------------------trial admin access--->>>>>>

# Admin Get All Programs
@program_blueprint.route('/admin/list-programs', methods=["GET"])
@jwt_required()
@role_required('admin')
def all_list_programs():
    try:
        # Mengambil semua program dari database
        programs = Program.query.all()

        # Mengonversi data program ke format JSON
        programs_data = [program.serialize() for program in programs]

        # Mengembalikan data program sebagai JSON
        return api_response(
            status_code=200,
            message='User-Admin successfully accessed list of all programs',
            data={'programs': programs_data}
        )

    except Exception as e:
        return api_response(
            status_code=500,
            message='Failed to fetch program data',
            data={'error': str(e)}
        )