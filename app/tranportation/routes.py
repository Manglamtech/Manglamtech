from . import bp
from app.model.transportation import Transportation
from database.database import db
from flask import request,jsonify
import math


@bp.route('/transportation', methods=['POST'])
def add_mehendi_artist():
    data = request.get_json()
    transportation_data = Transportation(
        name=data.get("name"),
        top_picks=data.get('top_picks'),
        price=data.get('price'),
        location=data.get('location'),
        reviews=data.get('reviews'),
        latitude=data.get("latitude"),
        longitude =data.get("longitude")
        
    )
    db.session.add(transportation_data)
    db.session.commit()
    return jsonify({'message': 'transportation added successfully!'}), 201

@bp.route('/transportations', methods=['GET'])
def get_transportations():
    top_picks = request.args.get('top_picks', default=None, type=str)
    best_review = request.args.get('best_review', default=None, type=float)
    lowest_price = request.args.get('lowest_price', default=None, type=str)
    user_lat = request.args.get('lat', default=None, type=float)
    user_lon = request.args.get('lon', default=None, type=float)
    max_distance = 10 

    query = Transportation.query

    if top_picks is not None:
        query = query.filter_by(top_picks=True)
    
    if best_review is not None:
        if 4.0 <= best_review <= 5.0:
            query = query.filter(Transportation.reviews >= best_review)
        else:
            return jsonify({'error': 'best_review must be between 4.0 and 5.0'}), 400
    
    if lowest_price is not None:
        query = query.filter(Transportation.price <= float(lowest_price))
    

    
    transportation=query.all()
    if user_lat is not None and user_lon is not None:

        filtered_transpoart = []
        for tr in transportation:
            tr_lat = tr.latitude  
            tr_lon = tr.longitude  
            distance = math.sqrt((user_lat - tr_lat)**2 + (user_lon - tr_lon)**2)
            if distance <= max_distance:
                filtered_transpoart.append(tr)
        transportation = filtered_transpoart

    result = [
        {
            'name': tr.name,
            'top_picks': tr.top_picks,
            'price': tr.price,
            'location': tr.location,
            'reviews': tr.reviews,
        
        } for tr in transportation
    ]
    
    return jsonify(result), 200

    


    

@bp.route('/transportations/<int:id>', methods=['GET'])
def get_transportation(id):
    transportation = Transportation.query.get_or_404(id)
    transportation_data = {
        'id': transportation.id,
        'name': transportation.name,
        'top_picks': transportation.top_picks,
        'price': transportation.price,
        'location': transportation.location,
        'reviews': transportation.reviews,
        
    }
    return jsonify(transportation_data)