from flask import Blueprint 

bp = Blueprint("notification" , __name__)

# from app.customer import routes
from . import routes