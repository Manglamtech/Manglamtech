from . import bp
from app.model.vendor import VENDOR
from database.database import db
from flask import request,jsonify
import math


@bp.route('/transportation/<string:service>', methods=['GET'])
def get_entertainments(service):
    service=VENDOR.query.filter_by(service=service).all()
    top_picks = request.args.get('top_picks', default=None, type=str)
    best_review = request.args.get('best_review', default=None, type=float)
    lowest_price = request.args.get('lowest_price', default=None, type=str)
    
    # query = VENDOR.query

    # if top_picks is not None:
    #     query = query.filter_by(top_picks=True)
    
    # if best_review is not None:
    #     if 4.0 <= best_review <= 5.0:
    #         query = query.filter(VENDOR.reviews <= best_review)
    #     else:
    #         return jsonify({'error': 'best_review must be between 4.0 and 5.0'}), 400
    
    # if lowest_price is not None: 
    #     query = query.filter(VENDOR.price <= float(lowest_price))

    # entertainments=query.all()

    output = []
    for themedecore in service:
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
