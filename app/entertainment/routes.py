from . import bp
from app.model.vendor import VENDOR
from database.database import db
from flask import request,jsonify



@bp.route('/entertainments/<string:service>', methods=['GET'])
def get_entertainments(service):
    try:
        entertainments=VENDOR.query.filter_by(service=service)
        location = request.args.get('location')
        if location:
            entertainments = entertainments.filter(VENDOR.location == location)
        
        entertainments = entertainments.all()
    

        output = []
        for entertainment in entertainments:
            entertainment_data = {
                # "id":entertainment.id,
                'person_name': entertainment.person_name,
                "email_id":entertainment.email_id,
                "phone_no":entertainment.phone_no
                # 'top_picks': entertainment.top_picks,
                # 'price': entertainment.price,
                # 'location': entertainment.location,
                # 'reviews': entertainment.reviews,
                
            }
            output.append(entertainment_data)
        
        return jsonify({'entertainments': output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500