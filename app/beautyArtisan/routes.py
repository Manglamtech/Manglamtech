from . import bp
from app.model.vendor import VENDOR
from database.database import db
from flask import request,jsonify


@bp.route('/beautyartisan/<string:service>', methods=['GET'])
def get_beautyartisan(service):
    try:
        beautyArtisan = VENDOR.query.filter_by(service=service)

        # Apply location filter if provided
        location = request.args.get('location')
        if location:
            beautyArtisan=  beautyArtisan.filter(VENDOR.location == location)
        
        beautyArtisan =  beautyArtisan.all()
        
        # Create the output list
        output = []
        for  beautyartisan in beautyArtisan:
            beautyartisan_data = {
                "id":beautyartisan.id,
                'person_name':beautyartisan.person_name,
                'email_id': beautyartisan.email_id,
                'phone_no': beautyartisan.phone_no,
                "location":beautyartisan.location
            }
            output.append(beautyartisan_data)
        
        return jsonify({'beautyartisan': output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500