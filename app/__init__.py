from flask import Flask
from app.controllers.program import program_route
from app.controllers.user_management_route import user_routes
from app.controllers.contact_management_route import contact_routes
from app.controllers.donation_management_route import donation_routes

import os
from app.utils.db import db
# from app.models import enclosure

app = Flask(__name__)

DATABASE_TYPE = os.getenv('DATABASE_TYPE')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_PORT = os.getenv('DATABASE_PORT')

# Perbaikan: Gunakan "SQLALCHEMY_DATABASE_URI" bukan "SQLALCHEMY_DATABASE_URL"
app.config["SQLALCHEMY_DATABASE_URI"] = f"{DATABASE_TYPE}://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

db.init_app(app)

# Perbaikan: Gunakan url_prefix yang benar sesuai kebutuhan Anda
app.register_blueprint(user_routes._blueprints, url_prefix='/')
app.register_blueprint(program_route.program_blueprint, url_prefix='/program')
app.register_blueprint(contact_routes._blueprints, url_prefix='/')
app.register_blueprint(donation_routes._blueprints, url_prefix='/')

# implementasi versioning api agar lebih ringkas bisa seperti ini, contohnya
# app.register_blueprint(animal_route.animal_blueprint, url_prefix='/v1/animal')

@app.route('/')
def my_app():

    return "Wellcome in my 6th Module"