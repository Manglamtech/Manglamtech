from . import bp
from app.model.digital_service import DigitalService
from database.database import db
from flask import request,jsonify
from sqlalchemy import asc, desc
import math


@bp.route('/digital_services', methods=['POST'])
def add_digital_service():
    data = request.get_json()
    new_digitalservice = DigitalService(
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
    db.session.add(new_digitalservice)
    db.session.commit()
    return jsonify({'message': 'digital service added successfully!'}), 201

@bp.route('/digital_services', methods=['GET'])
def get_digital_service():
    top_picks = request.args.get('top_picks', default=None, type=str)
    best_review = request.args.get('best_review', default=None, type=float)
    lowest_price = request.args.get('lowest_price', default=None, type=str)
    user_lat = request.args.get('lat', default=None, type=float)
    user_lon = request.args.get('lon', default=None, type=float)
    
    max_distance = 10
    query = DigitalService.query

    if top_picks is not None:
        query = query.filter_by(top_picks=True)
    
    if best_review is not None:
        if 4.0 <= best_review <= 5.0:
            query = query.filter(DigitalService.reviews >= best_review)
        else:
            return jsonify({'error': 'best_review must be between 4.0 and 5.0'}), 400
    
    if lowest_price is not None:
        query = query.filter(DigitalService.price <= float(lowest_price))
    

    digital_service=query.all()
    if user_lat is not None and user_lon is not None:
        filtered_digital_service = []
        for ds in digital_service:
            ds_lat = ds.latitude  
            ds_lon = ds.longitude  
            distance = math.sqrt((user_lat - ds_lat)**2 + (user_lon - ds_lon)**2)
            if distance <= max_distance:
                filtered_digital_service.append(ds)
        digital_service = filtered_digital_service


    result = [
        {
            'name': ds.name,
            'top_picks': ds.top_picks,
            'price': ds.price,
            'location': ds.location,
            'reviews': ds.reviews,
        
        } for ds in digital_service
    ]
    
    return jsonify(result), 200


