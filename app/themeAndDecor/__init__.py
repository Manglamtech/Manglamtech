from flask import Blueprint 

bp = Blueprint("themeAndDecore" , __name__)

# from app.customer import routes
from . import routes