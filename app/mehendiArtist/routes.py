from . import bp
from app.model.mehendiArtist import MehendiArtist
from database.database import db
from flask import request,jsonify
import math

@bp.route('/mehendi_artists', methods=['POST'])
def add_mehendi_artist():
    data = request.get_json()
    new_artist = MehendiArtist(
        name=data.get("name"),
        contact_information=data.get(" contact_information"),
        experience=data.get("experience"),
        top_picks=data.get('top_picks'),
        price=data.get('price'),
        location=data.get('location'),
        reviews=data.get('reviews'),
        latitude=data.get("latitude"),
        longitude =data.get("longitude"),
        availability_status=data.get("availability_status")

    )
    db.session.add(new_artist)
    db.session.commit()
    return jsonify({'message': 'Mehendi artist added successfully!'}), 201


    
@bp.route('/mehendi_artists', methods=['GET'])
def get_event_organizers():
    top_picks = request.args.get('top_picks', default=None, type=str)
    best_review = request.args.get('best_review', default=None, type=float)
    lowest_price = request.args.get('lowest_price', default=None, type=str)
    user_lat = request.args.get('lat', default=None, type=float)
    user_lon = request.args.get('lon', default=None, type=float)
    
    max_distance = 10  # Hardcoded maximum distance

    query = MehendiArtist.query
    
    if top_picks is not None:
        query = query.filter_by(top_picks=True)
    
    if best_review is not None:
        if 4.0 <= best_review <= 5.0:
            query = query.filter(MehendiArtist.reviews >= best_review)
        else:
            return jsonify({'error': 'best_review must be between 4.0 and 5.0'}), 400
    
    if lowest_price is not None:
        query = query.filter(MehendiArtist.price <= float(lowest_price))
    
    mehandi_artist = query.all()
    if user_lat is not None and user_lon is not None:
        filtered_artist = []
        for eo in mehandi_artist:
            eo_lat = eo.latitude  
            eo_lon = eo.longitude  
            distance = math.sqrt((user_lat - eo_lat)**2 + (user_lon - eo_lon)**2)
            if distance <= max_distance:
                filtered_artist.append(eo)
        mehandi_artist = filtered_artist

    result = [
        {
            'name': eo.name,
            "contact_information":eo.contact_information,
            'price': eo.price,
            'location': eo.location,
            'reviews': eo.reviews,
        
        } for eo in mehandi_artist
    ]
    
    return jsonify(result), 200