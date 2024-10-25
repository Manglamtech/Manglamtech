from . import bp
from app.model.rating import Rating
from database.database import db
from flask import request,jsonify
from sqlalchemy.exc import IntegrityError
from app.auth.routes import token_required, secret_key
import jwt



@bp.route('/rate', methods=['POST'])
@token_required
def add_rating():
     
       
    data = request.json
    auth_header = request.headers.get("Authorization")
    payload = auth_header.split(" ")[1]
        # print(payload)
    token = jwt.decode(payload, secret_key, algorithms=["HS256"])
        # print(token)
    cs_id = token["id"]
    vendor_id = data.get('vendor_id')
    rating = data.get('rating')
    customer_id=cs_id


    if not vendor_id or not customer_id or rating is None:
        return jsonify({'error': 'Missing required fields'}), 400

    new_rating = Rating(vendor_id=vendor_id, customer_id=cs_id, rating=rating)

    try:
        db.session.add(new_rating)
        db.session.commit()
        ratings = Rating.query.filter_by(vendor_id=vendor_id).all()

        # Calculate the average rating using a for loop
        total_rating = 0
        count = 0
        for r in ratings:
            total_rating += r.rating
            count += 1
        
        average_rating = total_rating / count if count > 0 else 0
        
        return jsonify({'message': 'Rating added successfully', 'average_rating': average_rating}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Failed to add rating'}), 500


@bp.route('/rating/<int:vendor_id>', methods=['GET'])
def get_vendor_ratings(vendor_id):
    try:
        ratings = Rating.query.filter_by(vendor_id=vendor_id).all()

        # Convert ratings to a list of dictionaries
        # ratings_list = [{'customer_id': r.customer_id, 'rating': r.rating} for r in ratings]

        total_rating = 0
        count = 0
        for r in ratings:
            total_rating += r.rating
            count += 1
        
        average_rating = total_rating / count if count > 0 else 0

        
        return jsonify({'vendor_id': vendor_id, "average_rating":average_rating}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

