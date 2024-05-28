
from datetime import datetime
from app.models.program import Program
from app.utils.db import db

class Program_repo():
    def get_all_programs(self):
        programs = Program.query.all()
        return programs

    def create_program(self, program):
        db.session.add(program)
        db.session.commit()
        return program

    def get_update_program(self, id, program):
        program_obj = Program.query.get(id)
        program_obj.nama_program = program.nama_program
        program_obj.lokasi_program = program.lokasi_program
        
        db.session.commit()
        return program_obj
    
    def delete_program(self, id):
        program_obj = Program.query.get(id)

        db.session.delete(program_obj)
        db.session.commit()
        return program_obj
    
    def search_programs(self, lokasi_program):
        programs = Program.query.filter(Program.lokasi_program.like(f"%{lokasi_program}%")).all()
        return programs