from flask import Blueprint 

bp = Blueprint("transportation" , __name__)

# from app.customer import routes
from . import routes