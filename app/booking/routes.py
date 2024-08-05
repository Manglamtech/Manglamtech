from app.model.booking import Booking
from database.database import db
from flask import request,jsonify
from . import bp
from app.auth.routes import token_required
import datetime
from app.model.vendor import VENDOR




@bp.route("/booking" ,methods= ["POST"], endpoint="create_booking")
@token_required
def create_booking():
    try:
        data = request.json
        entry =Booking(**data)
        db.session.add(entry)
        db.session.commit()

        return jsonify(entry.to_dict()), 201
    
    except Exception as e:
        return jsonify({"status": "Failed", "message": str(e)}), 500

@bp.route("/booking/event",methods=["GET"],endpoint="get_booking_event")
@token_required
def get_booking_event():
    bookings=Booking.query.all()
    result= []
    for booking_event in bookings:
        booking_data={
            "customer_id":booking_event.customer_id,
            "booking_number":booking_event.booking_number,
            "event_details":booking_event.event_details,
            "date_booking":booking_event.date_booking,
            "date_event":booking_event.date_event,
            "vendor_id":booking_event.vendor_id,
            "confirmation_vendor":booking_event.confirmation_vendor,
            "confirmation_details":booking_event.confirmation_details,
            "data_cancelation":booking_event.data_cancelation,
            
        }
        result.append(booking_data)
    return jsonify({"booking_events":result})
        

@bp.route("/booking/event/<booking_id>",methods=["GET"],endpoint="booking_event")
@token_required
def booking_event(booking_id):
    bookings=Booking.query.all(booking_id)
    result= []
    for booking_event in bookings:
        booking_data={
            "customer_id":booking_event.customer_id,
            "booking_number":booking_event.booking_number,
            "event_details":booking_event.event_details,
            "date_booking":booking_event.date_booking,
            "date_event":booking_event.date_event,
            "vendor_id":booking_event.vendor_id,
            "confirmation_vendor":booking_event.confirmation_vendor,
            "confirmation_details":booking_event.confirmation_details,
            "data_cancelation":booking_event.data_cancelation
        }
        result.append(booking_data)
    return jsonify({"booking_events":result})
        


@bp.route("/check_availability", methods=["POST"])
def check_availability():
    data = request.json
    date_event = data.get('date_event')
    event_details = data.get('event_details')
    location = data.get('location')
    guest=data.get("guest")
    menu_description=data.get("menu_description")
    plates=data.get("plates")



    
    # if not date_event or not event_details or not location:
    #     return jsonify({"error": "date_event, event_details, and location are required"}), 400
    
    # Query to get vendors by location
    # vendors = VENDOR.query.filter_by(location=location).all()
    # if not vendors:
    #     return jsonify({"available": True, "message": "The location is available."}), 200
    
    # Query to check bookings for the given date_event and event_type
    bookings = Booking.query.filter(Booking.date_event == date_event , Booking.event_details == event_details).all()
    booking_list = []
    
    if bookings:
        for booking in bookings:
            booking_data = {
                "date_event": booking.date_event,
                "event_details":booking.event_details
            }
            booking_list.append(booking_data)
    
    return jsonify({"bookings": booking_list})
    
    if bookings:
        return jsonify({"available": False, "message": "The booking is not available."}), 200
    else:
        return jsonify({"available": True, "message": "The booking is available."}), 200




