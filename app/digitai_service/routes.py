from . import bp
from app.model.vendor import VENDOR
from database.database import db
from flask import request,jsonify
from sqlalchemy import asc, desc
import math


@bp.route('/digital_service/<string:service>', methods=['GET'])
def get_digitalservice(service):
    try:
        digitalservices=VENDOR.query.filter_by(service=service)
        location = request.args.get('location')
        if location:
            digitalservices = digitalservices.filter(VENDOR.location == location)
        
        digitalservices = digitalservices.all()
        
    

        output = []
        for digitalservice in digitalservices:
            digital_service_data = {
    
                'person_name': digitalservice.person_name,
                "email_id":digitalservice.email_id,
                "phone_no":digitalservice.phone_no
                # 'top_picks': entertainment.top_picks,
                # 'price': entertainment.price,
                # 'location': entertainment.location,
                # 'reviews': entertainment.reviews,
                
            }
            output.append(digital_service_data)
        
        return jsonify({'digital_service': output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500