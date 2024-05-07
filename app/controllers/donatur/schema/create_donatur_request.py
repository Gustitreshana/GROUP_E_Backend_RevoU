from pydantic import BaseModel, Field
from typing import Optional

class Create_donatur_request(BaseModel):
    nama :  str = Field(...,description="Name of donatur",min_length=3,max_length=100)
    alamat : str = Field(...,description="Email of employee",min_length=3,max_length=100)
    nomor_telepon : str = Field(...,description="Nomor handphone of donatur",min_length=9,max_length=20)
