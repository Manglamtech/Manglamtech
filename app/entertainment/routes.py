from . import bp
from app.model.entertainment import Entertainment
from database.database import db
from flask import request,jsonify

@bp.route('/entertainments', methods=['POST'])
def add_entertainment():
    data = request.get_json()
    new_entertainment = Entertainment(
        name=data.get('name'),
        top_picks=data.get('top_picks'),
        price=data.get('price'),
        location=data.get('location'),
        reviews=data.get('reviews', 0.0),
        distance=data.get('distance')
    )
    db.session.add(new_entertainment)
    db.session.commit()
    return jsonify({'message': 'Entertainment added successfully!'}), 201


@bp.route('/entertainments', methods=['GET'])
def get_entertainments():
    top_pick=request.args.get("top_pick")
    best_review=request.args.get("best_review")
    near_me=request.args.get("near_me")
    lowest_price=request.args.get("lowest_price")
    
    query = Entertainment.query
    if top_pick:
        query = query.filter(Entertainment.top_picks>= float(top_pick))
    if best_review:
        query = query.filter(Entertainment.reviews <= best_review)
    if near_me:
        query = query.filter(Entertainment.distance >= float(near_me))
    if lowest_price:
        query = query.filter(Entertainment.price >= float(lowest_price))
    
    entertainment=query.all()
    entertainment_list=[service.to_dict() for service in entertainment]
    return jsonify(entertainment_list),200