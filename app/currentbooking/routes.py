from app.model.current_booking import Currentbooking
from database.database import db
from flask import request,jsonify
from . import bp
from app.auth.routes import token_required

@bp.route("/currentbooking",methods=["POST"],endpoint="create_booking")
@token_required
def current_booking():
    try:
        current_booking_data = request.json
        print(current_booking_data)
        entry = Currentbooking(**current_booking_data)
        
        db.session.add(entry)
        db.session.commit()
   
        return jsonify(entry.to_dict()), 201
    except Exception as e:
        return jsonify({"status": "Failed", "message": str(e)}), 500

