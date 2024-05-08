
from app.models.program import Program
from app.utils.db import db

class Program_repo():
    def get_list_program(self):
        programs = Program.query.all()
        return programs
    
    def create_program(self, program):
        db.session.add(program)
        db.session.commit()
        return program

    def get_update_program(self, id, program):
        program_obj = Program.query.get(id)
        program_obj.name = program.name
        program_obj.email = program.email
        program_obj.phone = program.phone
        program_obj.role = program.role
        program_obj.schedule = program.schedule
        
        db.session.commit()
        return program_obj
    
    def delete_program(self, id):
        program_obj = Program.query.get(id)

        db.session.delete(program_obj)
        db.session.commit()
        return program_obj
    
    def search_programs(self, name):
        programs = Program.query.filter(Program.name.like(f"%{name}%")).all()
        return programs