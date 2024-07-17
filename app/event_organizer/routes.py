from . import bp
from app.model.event_organizer import EventOrganizer
from database.database import db
from flask import request,jsonify
import math

@bp.route('/event_organizers', methods=['POST'])
def add_event_organizer():
    data = request.get_json()
    new_event_organizer = EventOrganizer(
        name=data.get('name'),
        contact_information=data.get(" contact_information"),
        experience=data.get("experience"),
        top_picks=data.get('top_picks'),
        price=data.get('price'),
        location=data.get('location'),
        reviews=data.get('reviews', 0.0),
        latitude=data.get("latitude"),
        longitude =data.get("longitude"),
        availability_status=data.get("availability_status")
        
    )
    db.session.add(new_event_organizer)
    db.session.commit()
    return jsonify({'message': 'Event organizer added successfully!'}), 201


@bp.route('/event_organizers', methods=['GET'])
def get_event_organizers():
    top_picks = request.args.get('top_picks', default=None, type=str)
    best_review = request.args.get('best_review', default=None, type=float)
    lowest_price = request.args.get('lowest_price', default=None, type=str)
    user_lat = request.args.get('lat', default=None, type=float)
    user_lon = request.args.get('lon', default=None, type=float)
    
    max_distance = 10  # Hardcoded maximum distance

    query = EventOrganizer.query
    
    if top_picks is not None:
        query = query.filter_by(top_picks=True)
    
    if best_review is not None:
        if 4.0 <= best_review <= 5.0:
            query = query.filter(EventOrganizer.reviews >= best_review)
        else:
            return jsonify({'error': 'best_review must be between 4.0 and 5.0'}), 400
    
    if lowest_price is not None:
        query = query.filter(EventOrganizer.price <=float(lowest_price) )
    
    
    event_organizers = query.all()
    if user_lat is not None and user_lon is not None:
        filtered_organizers = []
        for eo in event_organizers:
            eo_lat = eo.latitude  # Assuming latitude is stored in the database
            eo_lon = eo.longitude  # Assuming longitude is stored in the database
            distance = math.sqrt((user_lat - eo_lat)**2 + (user_lon - eo_lon)**2)
            if distance <= max_distance:
                filtered_organizers.append(eo)
        event_organizers = filtered_organizers
    else:
        event_organizers = query.all()

    result = [
        {
            'name': eo.name,
            'top_picks': eo.top_picks,
            'price': eo.price,
            'location': eo.location,
            'reviews': eo.reviews,
        
        } for eo in event_organizers
    ]
    
    return jsonify(result), 200