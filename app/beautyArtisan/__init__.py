from flask import Blueprint 

bp = Blueprint("beautyArtisan" , __name__)

# from app.customer import routes
from . import routes