from . import bp
from app.model.beautyartisan import BeautyArtisan
from database.database import db
from flask import request,jsonify
import math

@bp.route('/beauty_artisans', methods=['POST'])
def add_beauty_artisan():
    data = request.get_json()
    new_beauty_artisan = BeautyArtisan(
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
    db.session.add(new_beauty_artisan)
    db.session.commit()
    return jsonify({'message': 'Beauty artisan added successfully!'}), 201

@bp.route('/beauty_artisans', methods=['GET'])
def get_beauty_artisan():
    top_picks = request.args.get('top_picks', default=None, type=str)
    best_review = request.args.get('best_review', default=None, type=float)
    lowest_price = request.args.get('lowest_price', default=None, type=str)
    user_lat = request.args.get('lat', default=None, type=float)
    user_lon = request.args.get('lon', default=None, type=float)
    
    max_distance = 10  # Hardcoded maximum distance

    query = BeautyArtisan.query
    if top_picks is not None:
        query = query.filter_by(top_picks=True)
    
    if best_review is not None:
        if 4.0 <= best_review <= 5.0:
            query = query.filter(BeautyArtisan.reviews >= best_review)
        else:
            return jsonify({'error': 'best_review must be between 4.0 and 5.0'}), 400
    
    if lowest_price is not None:
        query = query.filter(BeautyArtisan.price <= float(lowest_price))
    
    
    
    beauty_artisans = query.all()

    if user_lat is not None and user_lon is not None:
        filtered_artisan = []
        for ba in beauty_artisans:
            ba_lat = ba.latitude  
            ba_lon = ba.longitude  
            distance = math.sqrt((user_lat - ba_lat)**2 + (user_lon - ba_lon)**2)
            if distance <= max_distance:
                filtered_artisan.append(ba)
        beauty_artisans = filtered_artisan

    result = [
        {
            'name': ba.name,
            'top_picks': ba.top_picks,
            'price': ba.price,
            'location': ba.location,
            'reviews': ba.reviews,
        
        } for ba in beauty_artisans
    ]
    
    return jsonify(result), 200

    

    