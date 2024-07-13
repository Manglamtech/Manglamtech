from . import bp
from app.model.themeAndDecore import ThemeAndDecor
from database.database import db
from flask import request,jsonify


@bp.route('/themeanddecor', methods=['POST'])
def add_theme_and_decor():
    data = request.get_json()
    new_theme_and_decor = ThemeAndDecor(
        name=data.get('name'),
        top_picks=data.get('top_picks'),
        price=data.get('price'),
        location=data.get('location'),
        reviews=data.get('reviews', 0.0),
        distance=data.get('distance')
    )
    db.session.add(new_theme_and_decor)
    db.session.commit()
    return jsonify({'message': 'Theme and decor added successfully!'}), 201

@bp.route('/themeanddecor', methods=['GET'])
def get_theme_and_decor():
    top_pick=request.args.get("top_pick")
    best_review=request.args.get("best_review")
    near_me=request.args.get("near_me")
    lowest_price=request.args.get("lowest_price")

    query = ThemeAndDecor.query

    if top_pick:
        query = query.filter(ThemeAndDecor.top_picks>= float(top_pick))
    if best_review:
        query = query.filter(ThemeAndDecor.reviews <= best_review)
    if near_me:
        query = query.filter(ThemeAndDecor.distance >= float(near_me))
    if lowest_price:
        query = query.filter(ThemeAndDecor.price >= float(lowest_price))

    themeanddecore=query.all()
    themeanddecore_list=[service.to_dict() for service in themeanddecore]
    return jsonify(themeanddecore_list),200
    
