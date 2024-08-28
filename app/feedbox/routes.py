from app.model.feed_box import Feedbox
from database.database import db
from flask import request,jsonify
from . import bp
from app.auth.routes import token_required,secret_key
import jwt


@bp.route('/feedbox', methods=['POST'],endpoint="add_feedbox")
# @token_required
def add_feedbox():
    data = request.get_json()
    name = data.get('name')
    email_id = data.get('email_id')
    events = data.get('events')

    if not name or not email_id or not events or not isinstance(events, list):
        return jsonify({"error": "Missing or invalid required fields"}), 400

    feedbox = Feedbox.create_feedbox(name, email_id, events)

    if feedbox:
        return jsonify({
            # "id": feedbox.id,
            "name": feedbox.name,
            "email_id": feedbox.email_id,
            "events": feedbox.events
        }), 201
    else:
        return jsonify({"error": "Email ID already exists"}), 409

