from . import bp
from app.model.vendor import VENDOR
from database.database import db
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
            event_organizer_data = {
                'person_name': eo.person_name,
                "email_id":eo.email_id,
                "phone_no":eo.phone_no

                
            }
            output.append(event_organizer_data)
        
        return jsonify({'evevt_organizer': output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500