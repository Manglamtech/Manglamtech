from app.model.event import EVENT
from database.database import db
from flask import request,jsonify
from . import bp
from app.auth.routes import token_required
import jwt


@bp.route("/create/event",methods=["POST"], endpoint="create_event")
# @token_required
def create_event():
    try:
        order_data = request.json
        # print(order_data)
        auth_header = request.headers.get('Authorization')
        # print(auth_header)
        payload=auth_header.split(" ")[1]
        print(payload)
    
    
        entry = EVENT(**order_data)

        
        db.session.add(entry)
        db.session.commit()
   
        return jsonify(entry.to_dict()), 201
    except Exception as e:
        return jsonify({"status": "Failed", "message": str(e)}), 500

    
@bp.route('/events', methods=['GET'],endpoint="get_all_events")
@token_required
def get_all_events():
    
    events = EVENT.query.all()
    output = []
    for event in events:
        event_data = {
            'event_code': event.event_code,
            'event': event.event,
            'customer_id': event.customer_id,
            'vendor_id': event.vendor_id,
            'booking_status': event.booking_status
        }
        output.append(event_data)
    return jsonify({'events': output})

@bp.route('/get_events', methods=['GET'],endpoint="get_events")
def get_event():
    customer_id = request.args.get('customer_id')
    vendor_id = request.args.get('vendor_id')

    events = []
    if customer_id:
        events = EVENT.query.filter_by(customer_id=customer_id).all()
    elif vendor_id:
        events = EVENT.query.filter_by(vendor_id=vendor_id).all()
    

    if not events:
        return jsonify({'message': 'Event not found'}), 404
    
    event_data_list = []
    for event in events:
        event_data = {
            'event_code': event.event_code,
            'event': event.event,
            'customer_id': event.customer_id,
            'vendor_id': event.vendor_id,
            'booking_status': event.booking_status
        }

        event_data_list.append(event_data)
    
    return jsonify({'event': event_data})



@bp.route('/events/<int:customer_id>', methods=['GET'],endpoint="get_event")
@token_required
def get_event(customer_id):
    event = EVENT.query.filter_by(customer_id=customer_id).first()
    if not event:
        return jsonify({'message': 'Event not found'}), 404
    event_data = {
        'event_code': event.event_code,
        'event': event.event,
        'customer_id': event.customer_id,
        'vendor_id': event.vendor_id,
        'booking_status': event.booking_status
    }
    return jsonify({'event': event_data})

@bp.route('/events/<int:customer_id>', methods=['PUT'],endpoint="update_event")
@token_required
def update_event(customer_id):
    data = request.get_json()
    event = EVENT.query.filter_by(customer_id=customer_id).first()
    if not event:
        return jsonify({'message': 'Event not found'}), 404
    event.event_code = data.get('event_code',event.event_code)
    event.event = data.get('event',event.event)
    event.customer_id = data.get('customer_id',event.customer_id)
    # event.vendor_id = data['vendor_id']
    event.booking_status = data.get('booking_status',event.booking_status)
    db.session.commit()
    return jsonify({'message': 'Event updated successfully'})

@bp.route('/events/<int:customer_id>', methods=['DELETE'],endpoint="event_delete")
@token_required
def delete_event(customer_id):
    event = EVENT.query.filter_by(customer_id=customer_id).first()
    if not event:
        return jsonify({'message': 'Event not found'}), 404
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted successfully'})
