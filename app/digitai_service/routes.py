from . import bp
from app.model.vendor import VENDOR
from database.database import db
from flask import request,jsonify
import requests
from app.model.rating import Rating
from sqlalchemy import asc, desc
import math



@bp.route('/digital_service/<string:service>', methods=['GET'])
def get_digitalservice(service):
    try:
        digitalservices=VENDOR.query.filter_by(service=service)
        location = request.args.get('location')
        if location:
            digitalservices = digitalservices.filter(VENDOR.location == location)
        min_rating = request.args.get('min_rating')
        
        
        
        digitalservices = digitalservices.all()
        
        output = []
        for digitalservice in digitalservices:
            ratings = Rating.query.filter_by(vendor_id=digitalservice.id).all()
            if ratings:
                total_ratings = sum(rating.rating for rating in ratings)
                avg_rating = total_ratings / len(ratings)
            else:
                avg_rating = None
            
            # Filter by rating if provided
            if min_rating and (avg_rating is None or avg_rating < float(min_rating)):
                continue
            digital_service_data = {
                "id":digitalservice.id,
                'person_name': digitalservice.person_name,
                "email_id":digitalservice.email_id,
                "phone_no":digitalservice.phone_no,
                "location":digitalservice.location,
                'average_rating': round(avg_rating, 2) if avg_rating is not None else 'No ratings yet'
                # 'top_picks': entertainment.top_picks,
                # 'price': entertainment.price,
                # 'location': entertainment.location,
                # 'reviews': entertainment.reviews,
                
            }
            output.append(digital_service_data)
        
        return jsonify({'digital_service': output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    



