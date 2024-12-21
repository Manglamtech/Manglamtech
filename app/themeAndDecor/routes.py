from . import bp
from app.model.vendor import VENDOR
from database.database import db
from app.model.rating import Rating
from flask import request,jsonify


@bp.route('/themeanddecore/<string:service>', methods=['GET'])
def get_themeanddecore(service):
    try:
        theme = VENDOR.query.filter_by(service=service)

        # Apply location filter if provided
        location = request.args.get('location')
        if location:
            theme = theme.filter(VENDOR.location == location)
        
        theme = theme.all()
        
        # Create the output list
        output = []
        for themedecore in theme:
            ratings = Rating.query.filter_by(vendor_id=themedecore.id).all()
            avg_rating = sum(rating.rating for rating in ratings) / len(ratings) if ratings else None
            
            themedecore_data = {
                "id":themedecore.id,
                'person_name': themedecore.person_name,
                'email_id': themedecore.email_id,
                'phone_no': themedecore.phone_no,
                "location":themedecore.location,
                'average_rating': round(avg_rating, 2) if avg_rating is not None else 'No ratings yet'
            }
            output.append(themedecore_data)
        
        return jsonify({'themeanddecore': output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500