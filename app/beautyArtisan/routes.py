from . import bp
from app.model.beautyartisan import BeautyArtisan
from database.database import db
from flask import request,jsonify


@bp.route('/beauty_artisans', methods=['POST'])
def add_beauty_artisan():
    data = request.get_json()
    new_beauty_artisan = BeautyArtisan(
        name=data.get('name'),
        top_picks=data.get('top_picks'),
        price=data.get('price'),
        location=data.get('location'),
        reviews=data.get('reviews', 0.0),
        distance=data.get('distance')
    )
    db.session.add(new_beauty_artisan)
    db.session.commit()
    return jsonify({'message': 'Beauty artisan added successfully!'}), 201

@bp.route('/beauty_artisans', methods=['GET'])
def get_beauty_artisan():
    top_pick=request.args.get("top_pick")
    best_review=request.args.get("best_review")
    near_me=request.args.get("near_me")
    lowest_price=request.args.get("lowest_price")

    query = BeautyArtisan.query
    if top_pick:
        query = query.filter(BeautyArtisan.top_picks>= float(top_pick))
    if best_review:
        query = query.filter(BeautyArtisan.reviews <= best_review)
    if near_me:
        query = query.filter(BeautyArtisan.distance >= float(near_me))
    if lowest_price:
        query = query.filter(BeautyArtisan.price >= float(lowest_price))
    
    
    beauty_artisans = BeautyArtisan.query.all()
    beauty_artisans_list=[service.to_dict() for service in beauty_artisans]
    return jsonify(beauty_artisans_list),200
    