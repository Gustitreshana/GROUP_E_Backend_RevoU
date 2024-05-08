from app.repositories.program_repo import Program_repo
from app.models.program import Program


class Program_service:
    def __init__(self):
        self.program_repo = Program_repo()
    
    def get_program(self):
        programs = self.program_repo.get_list_program()
        return [program.as_dict() for program in programs]

    def create_program(self, program_data_dto):
        program = Program()

        program.nama_program = program_data_dto.nama_program
        program.lokasi_program = program_data_dto.lokasi_program

        created_program = self.program_repo.create_program(program)
        return created_program.as_dict()

    def update_program(self, id, program_data_dto):
        update_program = self.program_repo.get_update_program(id, program_data_dto)
        return update_program.as_dict
    
    def delete_program(self, id):
        program = program.query.get(id)
        if not program:
            return "program not available"
        
        delete_program = self.program_repo.delete_program(id)
        return delete_program.as_dict()
    
    def search_programs(self, name):
        programs = self.program_repo.search_programs(name)
        return [program.as_dict() for program in programs]