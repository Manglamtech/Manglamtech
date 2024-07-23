from flask import Blueprint 

bp = Blueprint("rating" , __name__)

# from app.customer import routes
from . import routes