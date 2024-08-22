from flask import Blueprint 

bp = Blueprint("packages" , __name__)

# from app.customer import routes
from . import routes