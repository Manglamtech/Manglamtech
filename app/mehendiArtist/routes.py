from . import bp
from app.model.vendor import VENDOR
from database.database import db
from app.model.rating import Rating
from flask import request,jsonify



@bp.route('/mehendiartist/<string:service>', methods=['GET'])
def get_mehandiartist(service):
    try:
        mehendi_artists = VENDOR.query.filter_by(service=service)

        # Apply location filter if provided
        location = request.args.get('location')
        if location:
            mehendi_artists = mehendi_artists.filter(VENDOR.location == location)
        
        mehendi_artists = mehendi_artists.all()
        
        # Create the output list
        output = []
        for mendhiartist in mehendi_artists:
            ratings = Rating.query.filter_by(vendor_id=mendhiartist.id).all()
            avg_rating = sum(rating.rating for rating in ratings) / len(ratings) if ratings else None
            mendhiartist_data = {
                "id":mendhiartist.id,
                'person_name': mendhiartist.person_name,
                'email_id': mendhiartist.email_id,
                'phone_no': mendhiartist.phone_no,
                "location":mendhiartist.location,
                'average_rating': round(avg_rating, 2) if avg_rating is not None else 'No ratings yet'
            }
            output.append(mendhiartist_data)
        
        return jsonify({'mendhiartist': output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500