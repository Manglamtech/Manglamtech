from . import bp
from app.model.digital_service import DigitalService
from database.database import db
from flask import request,jsonify
from sqlalchemy import asc, desc
from math import radians, cos, sin, sqrt, atan2


@bp.route('/digital_services', methods=['POST'])
def add_digital_service():
    data = request.get_json()
    new_digitalservice = DigitalService(
        name=data.get('name'),
        top_picks=data.get('top_picks'),
        price=data.get('price'),
        location=data.get('location'),
        reviews=data.get('reviews', 0.0),
        distance=data.get('distance')
    )
    db.session.add(new_digitalservice)
    db.session.commit()
    return jsonify({'message': 'digital service added successfully!'}), 201

@bp.route('/digital_services', methods=['GET'])
def get_digital_service():
    top_pick=request.args.get("top_pick")
    best_review=request.args.get("best_review")
    near_me=request.args.get("near_me")
    lowest_price=request.args.get("lowest_price")
    query = DigitalService.query

    if top_pick:
        query = query.filter(DigitalService.top_picks>= float(top_pick))
    if best_review:
        query = query.filter(DigitalService.reviews <= best_review)
    if near_me:
        query = query.filter(DigitalService.distance >= float(near_me))
    if lowest_price:
        query = query.filter(DigitalService.price >= float(lowest_price))


    digital_service=query.all()
    list=[service.to_dict() for service in digital_service]
    return jsonify(list),200


