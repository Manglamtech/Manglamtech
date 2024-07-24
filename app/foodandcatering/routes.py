from . import bp
from app.model.vendor import VENDOR
from database.database import db
from app.model.rating import Rating
from flask import request,jsonify


@bp.route('/foodAndCatering/<string:service>', methods=['GET'])
def get_mehandiartist(service):
    try:
        catering = VENDOR.query.filter_by(service=service)

        # Apply location filter if provided
        location = request.args.get('location')
        if location:
            catering = catering.filter(VENDOR.location == location)
        
        catering = catering.all()
        
        # Create the output list
        output = []
        for foodAndCatering in catering:
            ratings = Rating.query.filter_by(vendor_id=foodAndCatering.id).all()
            avg_rating = sum(rating.rating for rating in ratings) / len(ratings) if ratings else None
            foodAndCatering_data = {
                "id":foodAndCatering.id,
                'person_name': foodAndCatering.person_name,
                'email_id': foodAndCatering.email_id,
                'phone_no': foodAndCatering.phone_no,
                "location":foodAndCatering.location,
                'average_rating': round(avg_rating, 2) if avg_rating is not None else 'No ratings yet'
            }
            output.append(foodAndCatering_data)
        
        return jsonify({'foodAndCatering': output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500