from . import bp
from app.model.themeAndDecore import ThemeAndDecor
from database.database import db
from flask import request,jsonify
import math


@bp.route('/themeanddecor', methods=['POST'])
def add_theme_and_decor():
    data = request.get_json()
    new_theme_and_decor = ThemeAndDecor(
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
    db.session.add(new_theme_and_decor)
    db.session.commit()
    return jsonify({'message': 'Theme and decor added successfully!'}), 201

@bp.route('/themeanddecor', methods=['GET'])
def get_theme_and_decor():
    top_picks = request.args.get('top_picks', default=None, type=str)
    best_review = request.args.get('best_review', default=None, type=float)
    lowest_price = request.args.get('lowest_price', default=None, type=str)
    user_lat = request.args.get('lat', default=None, type=float)
    user_lon = request.args.get('lon', default=None, type=float)
    
    max_distance = 10  # Hardcoded maximum distance
    
    query = ThemeAndDecor.query
    if top_picks is not None:
        query = query.filter_by(top_picks=True)
    
    if best_review is not None:
        if 4.0 <= best_review <= 5.0:
            query = query.filter(ThemeAndDecor.reviews >= best_review)
        else:
            return jsonify({'error': 'best_review must be between 4.0 and 5.0'}), 400
    
    if lowest_price is not None:
        query = query.filter(ThemeAndDecor.price <= float(lowest_price))

    

    themeanddecore=query.all()
    if user_lat is not None and user_lon is not None:
        filtered_theme = []
        for tm in themeanddecore:
            tm_lat = tm.latitude  
            tm_lon = tm.longitude  
            distance = math.sqrt((user_lat - tm_lat)**2 + (user_lon - tm_lon)**2)
            if distance <= max_distance:
                filtered_theme.append(tm)
        themeanddecore = filtered_theme

    result = [
        {
            'name': tm.name,
            'top_picks': tm.top_picks,
            'price': tm.price,
            'location': tm.location,
            'reviews': tm.reviews,
        
        } for tm in themeanddecore
    ]
    
    return jsonify(result), 200
