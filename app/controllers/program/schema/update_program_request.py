from pydantic import BaseModel, Field
from typing import Optional

class Update_program_request(BaseModel):
    nama_program :  str = Field(...,description="Name of program donate",min_length=6,max_length=100)
    lokasi_program : str = Field(...,description="Locate of program donate",min_length=10,max_length=200)