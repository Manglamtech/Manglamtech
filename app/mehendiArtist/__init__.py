from flask import Blueprint 

bp = Blueprint("mehandiartist" , __name__)

# from app.customer import routes
from . import routes