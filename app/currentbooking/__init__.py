from flask import Blueprint 

bp = Blueprint("currentbooking" , __name__)

from . import routes