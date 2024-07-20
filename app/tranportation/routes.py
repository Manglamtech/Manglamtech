from . import bp
from app.model.vendor import VENDOR
from database.database import db
from flask import request,jsonify


@bp.route('/transportation/<string:service>', methods=['GET'])
def get_transportation(service):
    try:
        transportations=VENDOR.query.filter_by(service=service)

        location = request.args.get('location')
        if location:
            transportations= transportations.filter(VENDOR.location == location)
        
        transportations = transportations.all()
        

    

        output = []
        for transportation in transportations:
            transportation_data = {
                "id":transportation.id,
                'person_name':transportation.person_name,
                "email_id":transportation.email_id,
                "phone_no":transportation.phone_no
                # 'top_picks': entertainment.top_picks,
                # 'price': entertainment.price,
                # 'location': entertainment.location,
                # 'reviews': entertainment.reviews,
                
            }
            output.append(transportation_data)
        
        return jsonify({'transportation': output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    