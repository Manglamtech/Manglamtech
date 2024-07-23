from flask import Blueprint 

bp = Blueprint("food and catering" , __name__)

# from app.customer import routes
from . import routes