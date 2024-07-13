from . import bp
from app.model.event_organizer import EventOrganizer
from database.database import db
from flask import request,jsonify

@bp.route('/event_organizers', methods=['POST'])
def add_event_organizer():
    data = request.get_json()
    new_event_organizer = EventOrganizer(
        name=data.get('name'),
        top_picks=data.get('top_picks'),
        price=data.get('price'),
        location=data.get('location'),
        reviews=data.get('reviews', 0.0),
        distance=data.get('distance')
    )
    db.session.add(new_event_organizer)
    db.session.commit()
    return jsonify({'message': 'Event organizer added successfully!'}), 201


@bp.route('/event_organizers', methods=['GET'])
def get_event_organizers():
    top_pick=request.args.get("top_pick")
    best_review=request.args.get("best_review")
    near_me=request.args.get("near_me")
    lowest_price=request.args.get("lowest_price")

    query = EventOrganizer.query
    if top_pick:
        query = query.filter(EventOrganizer.top_picks>= float(top_pick))
    if best_review:
        query = query.filter(EventOrganizer.reviews <= best_review)
    if near_me:
        query = query.filter(EventOrganizer.distance >= float(near_me))
    if lowest_price:
        query = query.filter(EventOrganizer.price >= float(lowest_price))

    eventorganizer=query.all()
    eventorganizer_list=[service.to_dict() for service in eventorganizer]
    
    return jsonify({'event_organizers': eventorganizer_list})