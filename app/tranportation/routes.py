from . import bp
from app.model.transportation import Transportation
from database.database import db
from flask import request,jsonify


@bp.route('/transportation', methods=['POST'])
def add_mehendi_artist():
    data = request.get_json()
    transportation_data = Transportation(
        name=data.get("name"),
        top_picks=data.get('top_picks'),
        price=data.get('price'),
        location=data.get('location'),
        reviews=data.get('reviews'),
        distance=data.get('distance')
    )
    db.session.add(transportation_data)
    db.session.commit()
    return jsonify({'message': 'transportation added successfully!'}), 201

@bp.route('/transportations', methods=['GET'])
def get_transportations():
    top_pick=request.args.get("top_pick")
    best_review=request.args.get("best_review")
    near_me=request.args.get("near_me")
    lowest_price=request.args.get("lowest_price")

    query = Transportation.query

    if top_pick:
        query = query.filter(Transportation.top_picks>= float(top_pick))
    if best_review:
        query = query.filter(Transportation.reviews <= best_review)
    if near_me:
        query = query.filter(Transportation.distance >= float(near_me))
    if lowest_price:
        query = query.filter(Transportation.price >= float(lowest_price))

    transportation=query.all()
    transportation_list=[service.to_dict() for service in transportation]
    return jsonify(transportation_list),200


    

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
        'distance': transportation.distance
    }
    return jsonify(transportation_data)