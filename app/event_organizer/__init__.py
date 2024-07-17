from flask import Blueprint 

bp = Blueprint("event_organizer" , __name__)

# from app.customer import routes
from . import routes