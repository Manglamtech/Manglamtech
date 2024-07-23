from . import bp
from app.model.vendor import VENDOR
from database.database import db
from app.model.rating import Rating
from flask import request,jsonify



@bp.route('/themanddecor/<string:service>', methods=['GET'])
def get_themanddecor(service):
    try:
        themeanddecore=VENDOR.query.filter_by(service=service).all()
        location = request.args.get('location')
        if location:
            themeanddecore = themeanddecore.filter(VENDOR.location == location)

        themeanddecore=themeanddecore.all()

    
        output = []
        for themedecore in themeanddecore:
            ratings = Rating.query.filter_by(vendor_id=themeanddecore.id).all()
            avg_rating = sum(rating.rating for rating in ratings) / len(ratings) if ratings else None
            themeandDecore_data = {
                "id":themedecore.id,
                'person_name':themedecore.person_name,
                "email_id":themedecore.email_id,
                "phone_no":themedecore.phone_no,
                "location":themeanddecore.location,
                'average_rating': round(avg_rating, 2) if avg_rating is not None else 'No ratings yet'
                # 'top_picks': entertainment.top_picks,
                # 'price': entertainment.price,
                # 'location': entertainment.location,
                # 'reviews': entertainment.reviews,
                
            }
            output.append(themeandDecore_data)
    
        return jsonify({'themeAndDecore': output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500