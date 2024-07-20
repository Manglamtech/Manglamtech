from . import bp
from app.model.vendor import VENDOR
from database.database import db
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
            mendhiartist_data = {
                'person_name': mendhiartist.person_name,
                'email_id': mendhiartist.email_id,
                'phone_no': mendhiartist.phone_no
            }
            output.append(mendhiartist_data)
        
        return jsonify({'mendhiartist': output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500