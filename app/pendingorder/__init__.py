from flask import Blueprint 

bp = Blueprint("pending" , __name__)

# from app.customer import routes
from . import routes