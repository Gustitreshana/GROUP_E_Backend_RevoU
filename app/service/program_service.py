from datetime import datetime
from app.repositories.program_repo import Program_repo
from app.models.program import Program
from app.models.user import User

class Program_service:
    def __init__(self):
        self.program_repo = Program_repo()
    
    # def get_programs(self, user_id):
    #     # Mengambil objek User berdasarkan user_id
    #     user = User.query.get(user_id)
    #     if not user:
    #         raise ValueError(f"Tidak dapat menemukan user dengan ID {user_id}")
        
    #     programs = self.program_repo.get_list_program()
    #     return [program.serialize() for program in programs]

    def get_programs(self, user_id):
        # Mengambil objek User berdasarkan user_id
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"Tidak dapat menemukan user dengan ID {user_id}")

        # Memastikan bahwa user memiliki peran 'Admin'
        if user.role != 'Admin':
            raise PermissionError("User tidak memiliki hak akses untuk melihat program")

        # Mengambil semua program dari repository
        programs = self.program_repo.get_all_programs()
        return programs

    def create_program(self, program_data_dto, user_id):
        # Mengambil objek User berdasarkan user_id
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"Tidak dapat menemukan user dengan ID {user_id}")

        # Membuat objek Program dengan data yang diberikan
        program = Program()

        program.nama_program=program_data_dto.nama_program
        program.lokasi_program=program_data_dto.lokasi_program
        program.user=user  # Mengatur objek User
        program.created_at=datetime.now()
        program.updated_at=datetime.now()
        

        # Menyimpan program baru ke database
        created_program = self.program_repo.create_program(program)
        return created_program.serialize()

    def update_program(self, id, program_data_dto):
        update_program = self.program_repo.get_update_program(id, program_data_dto)
        return update_program.serialize()
    
    def delete_program(self, id):
        program = program.query.get(id)
        if not program:
            return "program not available"
        
        delete_program = self.program_repo.delete_program(id)
        return delete_program.serialize()
    
    def search_programs(self, name):
        programs = self.program_repo.search_programs(name)
        return [program.serialize() for program in programs]