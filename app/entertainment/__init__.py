from flask import Blueprint 

bp = Blueprint("entertainment" , __name__)

# from app.customer import routes
from . import routes