from . import bp
from app.model.pandingorder import Pendingorder
from app.model.notification import Notification
from app.model.customer import User
from database.database import db
from flask import request,jsonify
from sqlalchemy.exc import IntegrityError
from app.auth.routes import token_required,secret_key
import jwt
import datetime
from datetime import datetime
from datetime import datetime, timedelta




# @bp.route("/pendingorder",methods=["POST"],endpoint="post_pending_order")
# @token_required
# def pendingorder():
    
#     try:
#         order_data = request.json
#         auth_header = request.headers.get('Authorization')
#         payload=auth_header.split(" ")[1]
#         # print(payload)
#         token = jwt.decode(payload, secret_key, algorithms=['HS256'])
#         # print(token)
#         cs_id= token["id"]

#         entry=Pendingorder(event_type=order_data.get("event_type"),address=order_data.get("address"),enter_preferences=order_data.get("enter_preferences"),phone_no=order_data.get("phone_no"),city=order_data.get("city"),date=order_data.get("date"),time=order_data.get("time"),customer_id=cs_id,status=order_data.get("status"))
#         db.session.add(entry)
#         db.session.commit()
   
#         return jsonify(entry.to_dict()), 201
    
#     except Exception as e:
#         return jsonify({"status": "Failed", "message": str(e)}), 500
    

@bp.route("/getpendingorder",methods=["GET"],endpoint="get_pending_order")
@token_required
def get_pendingorder():
    # auth_header = request.headers.get('Authorization')
    # payload=auth_header.split(" ")[1]
    #     # print(payload)
    # token = jwt.decode(payload, secret_key, algorithms=['HS256'])
    #     # print(token)
    # cs_id= token["id"]


    seven_days_ago = datetime.now() - timedelta(days=7)
    # user = User.query.get(cs_id)
    orders=Pendingorder.query.all()
    output=[]
    for order in orders:
        order_datetime = datetime.strptime(f"{order.date} {order.time}", '%Y-%m-%d %H:%M')
        if order_datetime < seven_days_ago:
            db.session.delete(order)
            continue
        customer = User.query.get(order.customer_id)
        if customer:
            customer_data = customer.to_dict()
        else:
            customer_data = None
        order_data={
            "id":order.id,
            "event_type":order.event_type,
            "address":order.address,
            "enter_preferences":order.enter_preferences,
            "phone_no":order.phone_no,
            "city":order.city,
            " date":order.date,
            "time":order.time,
            "customer_id":order.customer_id,
            "created_by":customer_data


        }
        output.append(order_data)
    db.session.commit()

    return jsonify({'notifications': output})



@bp.route('/upcoming_events', methods=['GET'],endpoint="upcoming_event")
@token_required
def get_upcoming_events():
    try:
        # Get the current date and time
        current_datetime = datetime.now()

        upcoming_events = Pendingorder.query.filter(
            Pendingorder.status == True 
        ).all()
        output = []
        for event in upcoming_events:
            # Check if the event's date and time are in the future
            event_datetime = datetime.strptime(f"{event.date} {event.time}", '%Y-%m-%d %H:%M')
            if event_datetime > current_datetime:
                event_data = {
                    "id": event.id,
                    "event_type": event.event_type,
                    "address": event.address,
                    "enter_preferences": event.enter_preferences,
                    "phone_no": event.phone_no,
                    "city": event.city,
                    "date": event.date,
                    "time": event.time,
                    "customer_id": event.customer_id,
                    "status": event.status
                }
                output.append(event_data)

        return jsonify({'upcoming_events': output}), 200

    except Exception as e:
        return jsonify({"status": "Failed", "message": str(e)}), 500


@bp.route('/past_events', methods=['GET'],endpoint="past_event")
@token_required
def get_past_events():
    try:
        current_datetime = datetime.now()

        upcoming_events = Pendingorder.query.filter(
            Pendingorder.status == True 
        ).all()

        output = []
        for event in upcoming_events:
            # Check if the event's date and time are in the future
            event_datetime = datetime.strptime(f"{event.date} {event.time}", '%Y-%m-%d %H:%M')
            if event_datetime < current_datetime:
                event_data = {
                    "id": event.id,
                    "event_type": event.event_type,
                    "address": event.address,
                    "enter_preferences": event.enter_preferences,
                    "phone_no": event.phone_no,
                    "city": event.city,
                    "date": event.date,
                    "time": event.time,
                    "customer_id": event.customer_id,
                    "status": event.status
                }
                output.append(event_data)

        return jsonify({'upcoming_events': output}), 200

    except Exception as e:
        return jsonify({"status": "Failed", "message": str(e)}), 500
    
