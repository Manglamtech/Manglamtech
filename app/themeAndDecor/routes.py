from . import bp
from app.model.vendor import VENDOR
from database.database import db
from flask import request,jsonify
import math


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
            themeandDecore_data = {
                "id":themedecore.id,
                'person_name':themedecore.person_name,
                "email_id":themedecore.email_id,
                "phone_no":themedecore.phone_no
                # 'top_picks': entertainment.top_picks,
                # 'price': entertainment.price,
                # 'location': entertainment.location,
                # 'reviews': entertainment.reviews,
                
            }
            output.append(themeandDecore_data)
    
        return jsonify({'themeAndDecore': output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500