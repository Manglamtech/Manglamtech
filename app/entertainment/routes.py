from . import bp
from app.model.entertainment import Entertainment
from database.database import db
from flask import request,jsonify
import math

@bp.route('/entertainments', methods=['POST'])
def add_entertainment():
    data = request.get_json()
    new_entertainment = Entertainment(
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
    db.session.add(new_entertainment)
    db.session.commit()
    return jsonify({'message': 'Entertainment added successfully!'}), 201


@bp.route('/entertainments', methods=['GET'])
def get_entertainments():
    top_picks = request.args.get('top_picks', default=None, type=str)
    best_review = request.args.get('best_review', default=None, type=float)
    lowest_price = request.args.get('lowest_price', default=None, type=str)
    user_lat = request.args.get('lat', default=None, type=float)
    user_lon = request.args.get('lon', default=None, type=float)
    max_distance = 10
    query = Entertainment.query

    if top_picks is not None:
        query = query.filter_by(top_picks=True)
    
    if best_review is not None:
        if 4.0 <= best_review <= 5.0:
            query = query.filter(Entertainment.reviews <= best_review)
        else:
            return jsonify({'error': 'best_review must be between 4.0 and 5.0'}), 400
    
    if lowest_price is not None:
        query = query.filter(Entertainment.price <= float(lowest_price))

    entertainment=query.all()

    if user_lat is not None and user_lon is not None:
        filtered_entertainment = []
        for en in entertainment:
            en_lat = en.latitude  
            en_lon = en.longitude  
            distance = math.sqrt((user_lat - en_lat)**2 + (user_lon - en_lon)**2)
            if distance <= max_distance:
                filtered_entertainment.append(en)
        entertainment =filtered_entertainment

    result = [
        {
            'name': en.name,
            'top_picks': en.top_picks,
            'price': en.price,
            'location': en.location,
            'reviews': en.reviews,
        
        } for en in entertainment
    ]
    
    return jsonify(result), 200
