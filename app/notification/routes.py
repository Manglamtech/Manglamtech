from . import bp
from app.model.notification import Notification
from database.database import db
from flask import request,jsonify
from sqlalchemy.exc import IntegrityError
from app.auth.routes import token_required,secret_key
import jwt

@bp.route("/notification",methods=["POST"])
@token_required
def get_notification():
    
    try:
        order_data = request.json
        auth_header = request.headers.get('Authorization')
        payload=auth_header.split(" ")[1]
        # print(payload)
        token = jwt.decode(payload, secret_key, algorithms=['HS256'])
        # print(token)
        cs_id= token["id"]

        entry=Notification(event_type=order_data.get("event_type"),address=order_data.get("address"),enter_preferences=order_data.get("enter_preferences"),phone_no=order_data.get("phone_no"),city=order_data.get("city"),date=order_data.get("date"),time=order_data.get("time"),customer_id=cs_id)
        db.session.add(entry)
        db.session.commit()
   
        return jsonify(entry.to_dict()), 201
        
        
    except Exception as e:
        return jsonify({"status": "Failed", "message": str(e)}), 500
    

@bp.route("/getNotification",methods=["get"],endpoint="get_all notification")
def get_all_notification():
    notifications=Notification.query.all()
    output=[]
    for notification in notifications:
        notification_data={
            "id":notification.id,
            "event_type":notification.event_type,
            "address":notification.address,
            "enter_preferences":notification.enter_preferences,
            "phone_no":notification.phone_no,
            "city":notification.city,
            " date":notification.date,
            "time":notification.time,
            "customer_id":notification.customer_id


        }
        output.append(notification_data)
    return jsonify({'notification_data': output})