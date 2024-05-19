from flask import Blueprint, jsonify, request, json
# from app.utils.database import db
from app.models.program import Program
from app.service.program_service import Program_service
from app.utils.api_response import api_response
from app.controllers.program.schema.create_program_request import Create_program_request
from app.controllers.program.schema.update_program_request import Update_program_request
from pydantic import ValidationError

program_blueprint = Blueprint('program_endpoint', __name__)

@program_blueprint.route('/', methods=['POST'])
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

        Update_program_request = Create_program_request(**data)

        program_service = Program_service()

        programs = program_service.create_program(Update_program_request)

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
    
@program_blueprint.route('/', methods=['GET'])
def get_programs():
    try:
        
        program_service = Program_service()
        programs = program_service.get_programs()
        # return programs
        return api_response(
            status_code = 200,
            message ="Daftar semua programs sukses diakses",
            data = programs
        )
    
    except Exception as e:
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )   
    
@program_blueprint.route('//<int:program_id>', methods=['GET'])
def get_program(program_id):
    try:
        program = Program.query.get(program_id)
        if program:
            return api_response(
                status_code=200,
                message="Daftar data dari id karyawan berhasil ditampilkan",
                data=[program.as_dict()]
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

@program_blueprint.route('//<int:program_id>', methods=['PUT'])
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

@program_blueprint.route('/<int:program_id>', methods=['DELETE'])
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
            message="Data karyawan berhasil dihapus (sudah resign)",
            data=program
        )    
        
    except Exception as e:
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        ) 
    
@program_blueprint.route('/search', methods=['GET'])
def search_programs():
    try:
        request_data = request.args
        
        program_service = Program_service()
        programs = program_service.search_programs(request_data['name'])
        if programs:
        # return [animal.as_dict() for animal in animals], 200
            return api_response(
                status_code=200,
                message="Daftar data karyawan yang dicari sukses diakses",
                data=programs
            )  
        else:
            return api_response(
                status_code=400,
                message="Data karyawan yang dicari tidak ditemukan",
                data={}
            )   
    except Exception as e:
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )       
