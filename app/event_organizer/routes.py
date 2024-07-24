from . import bp
from app.model.vendor import VENDOR
from database.database import db
from app.model.rating import Rating
from flask import request,jsonify


@bp.route('/event_organizer/<string:service>', methods=['GET'])
def get_event_organizer(service):
    try:
        eventOrganizer=VENDOR.query.filter_by(service=service)
        location = request.args.get('location')
        if location:
            eventOrganizer = eventOrganizer.filter(VENDOR.location == location)
        
        eventOrganizer = eventOrganizer.all()
    

        output = []
        for eo in eventOrganizer:
            ratings = Rating.query.filter_by(vendor_id=eo.id).all()
            avg_rating = sum(rating.rating for rating in ratings) / len(ratings) if ratings else None
            
            event_organizer_data = {
                "id":eo.id,
                'person_name': eo.person_name,
                "email_id":eo.email_id,
                "phone_no":eo.phone_no,
                "location":eo.location,
                'average_rating': round(avg_rating, 2) if avg_rating is not None else 'No ratings yet'

                
            }
            output.append(event_organizer_data)
        
        return jsonify({'evevt_organizer': output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500