from . import bp
from app.model.vendor import VENDOR
from database.database import db
from flask import request,jsonify
from app.model.rating import Rating


@bp.route('/venubooking/<string:service>', methods=['GET'])
def get_transportation(service):
    try:
        venu=VENDOR.query.filter_by(service=service)

        location = request.args.get('location')
        if location:
            venu= venu.filter(VENDOR.location == location)
        
        venu = venu.all()
        

    

        output = []
        for venu_booking in venu:
            ratings = Rating.query.filter_by(vendor_id=venu_booking.id).all()
            avg_rating = sum(rating.rating for rating in ratings) / len(ratings) if ratings else None
            venu_booking_data = {
                "id":venu_booking.id,
                'person_name':venu_booking.person_name,
                "email_id":venu_booking.email_id,
                "phone_no":venu_booking.phone_no,
                "location":venu_booking.location,
                'average_rating': round(avg_rating, 2) if avg_rating is not None else 'No ratings yet'
                # 'top_picks': entertainment.top_picks,
                # 'price': entertainment.price,
                # 'location': entertainment.location,
                # 'reviews': entertainment.reviews,
                
            }
            output.append(venu_booking_data)
        
        return jsonify({'venu_booking': output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    