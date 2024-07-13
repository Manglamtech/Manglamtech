from flask import Blueprint 

bp = Blueprint("digitalservice" , __name__)

# from app.customer import routes
from . import routes