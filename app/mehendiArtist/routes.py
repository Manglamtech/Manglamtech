from . import bp
from app.model.mehendiArtist import MehendiArtist
from database.database import db
from flask import request,jsonify


@bp.route('/mehendi_artists', methods=['POST'])
def add_mehendi_artist():
    data = request.get_json()
    new_artist = MehendiArtist(
        name=data.get("name"),
        top_picks=data.get('top_picks'),
        price=data.get('price'),
        location=data.get('location'),
        reviews=data.get('reviews'),
        distance=data.get('distance')
    )
    db.session.add(new_artist)
    db.session.commit()
    return jsonify({'message': 'Mehendi artist added successfully!'}), 201

@bp.route('/mehendi_artists', methods=['GET'])
def get_mehendi_artists():
    top_pick=request.args.get("top_pick")
    best_review=request.args.get("best_review")
    near_me=request.args.get("near_me")
    lowest_price=request.args.get("lowest_price")
    
    query= MehendiArtist.query
    if top_pick:
        query = query.filter(MehendiArtist.top_picks>= float(top_pick))
    if best_review:
        query = query.filter(MehendiArtist.reviews <= best_review)
    if near_me:
        query = query.filter(MehendiArtist.distance >= float(near_me))
    if lowest_price:
        query = query.filter(MehendiArtist.price >= float(lowest_price))
    
    mehendiartist=query.all()
    mendhiartist_list=[service.to_dict() for service in mehendiartist]
    return jsonify(mendhiartist_list),200