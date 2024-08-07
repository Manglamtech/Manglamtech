from flask import Blueprint 

bp = Blueprint("feedbox" , __name__)

from . import routes
