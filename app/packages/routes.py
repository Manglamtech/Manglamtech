from . import bp
from app.model.vendor import VENDOR
from database.database import db
from app.model.rating import Rating
from flask import request,jsonify



@bp.route('/packages/<string:service>', methods=['GET'])
def get_packages(service):
    try:
        package = VENDOR.query.filter_by(service=service)

        # Apply location filter if provided
        location = request.args.get('location')
        if location:
            package = package.filter(VENDOR.location == location)
        
        package = package.all()
        
        # Create the output list
        output = []
        for packages in package:
            ratings = Rating.query.filter_by(vendor_id=packages.id).all()
            avg_rating = sum(rating.rating for rating in ratings) / len(ratings) if ratings else None
            packages_data = {
                "id":packages.id,
                'person_name': packages.person_name,
                'email_id': packages.email_id,
                'phone_no': packages.phone_no,
                "location":packages.location,
                'average_rating': round(avg_rating, 2) if avg_rating is not None else 'No ratings yet'
            }
            output.append(packages_data)
        
        return jsonify({'packages_data': output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500