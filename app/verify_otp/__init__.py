from flask import Blueprint 

bp = Blueprint("verify_otp" , __name__)

# from app.customer import routes
from . import routes