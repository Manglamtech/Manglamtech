from . import bp
from app.model.rating import Rating
from database.database import db
from flask import request,jsonify
from sqlalchemy.exc import IntegrityError



@bp.route('/rate', methods=['POST'])
def add_rating():
    data = request.json
    vendor_id = data.get('vendor_id')
    customer_id = data.get('customer_id')
    rating = data.get('rating')


    if not vendor_id or not customer_id or rating is None:
        return jsonify({'error': 'Missing required fields'}), 400

    new_rating = Rating(vendor_id=vendor_id, customer_id=customer_id, rating=rating)

    try:
        db.session.add(new_rating)
        db.session.commit()
        return jsonify({'message': 'Rating added successfully'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Failed to add rating'})


@bp.route('/averagerating/<int:vendor_id>', methods=['GET'])
def get_average_rating(vendor_id):
    ratings = Rating.query.filter_by(vendor_id=vendor_id).all()
    
    if not ratings:
        return jsonify({'message': 'No ratings found for this vendor'}), 404
    
    total_ratings = 0
    rating_count = 0
    
    for rating in ratings:
        total_ratings += rating.rating
        rating_count += 1
    
    average_rating = total_ratings / rating_count
    
    return jsonify({'vendor_id': vendor_id, 'average_rating': round(average_rating, 2)}), 200