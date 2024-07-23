from flask import Blueprint 

bp = Blueprint("venu_booking" , __name__)

# from app.customer import routes
from . import routes