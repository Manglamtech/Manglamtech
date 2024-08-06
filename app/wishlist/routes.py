from app.model.wishlist import WishlistItem
from app.model.vendor import VENDOR
from database.database import db
from app.model.customer import User
import datetime
from flask import request,jsonify
from . import bp
from app.auth.routes import token_required,secret_key
import jwt
from sqlalchemy.exc import IntegrityError
from app.model.rating import Rating




@bp.route("/wishlist", methods=["POST"],endpoint="add_wishlist_item")
@token_required
def add_wishlist_item():
    auth_header = request.headers.get('Authorization')
    payload=auth_header.split(" ")[1]
    token = jwt.decode(payload, secret_key, algorithms=['HS256'])

    customer_id=token["id"]
    cs_id=customer_id
    user = User.query.get(cs_id)
    if not user:
        return jsonify({"error": "Invalid user ID"}), 400
    # current_date=str(datetime.datetime.now())
    data = request.get_json()
    vendor_service_id=data.get("vendor_service_id")
    if not vendor_service_id:
        return jsonify({"error":"vendor service id is required"}), 400
    existing_item = WishlistItem.query.filter_by(customer_id=cs_id, vendor_service_id=vendor_service_id).first()
    if existing_item:
        return jsonify({"error": "Item already in wishlist"}), 409
    
    wishlist_item = WishlistItem(customer_id=cs_id, vendor_service_id=vendor_service_id)
    db.session.add(wishlist_item)
    db.session.commit()
    vendor = VENDOR.query.get(vendor_service_id)
    if not vendor:
        return jsonify({"error": "Vendor not found"}), 404

    vendor_info = {
        "organization_name": vendor.organization_name,
        "person_name": vendor.person_name,
        "full_address": vendor.full_address,
        "email_id": vendor.email_id,
        "phone_no": vendor.phone_no,
        "service": vendor.service,
        "location": vendor.location,
        "gst_no": vendor.gst_no
        }
        
    return jsonify({"message": "Added to wishlist", "vendor": vendor_info}), 201
        
   

# @bp.route("/wishlist/<event>",methods=["GET"],endpoint="get_wishlist")
# @token_required
# def get_wishlist(event):
#     items = WishlistItem.query.filter_by(event=event).all()
#     result = [{"id": item.id, "event": item.event, "item": item.item, "quantity": item.quantity, "created_at": item.created_at} for item in items]
#     return jsonify(result), 200


# @bp.route('/wishlist/<int:id>', methods=['DELETE'],endpoint="delete_wishlist_item")
# @token_required
# def delete_wishlist_item(id):
#     item = WishlistItem.query.get(id)
#     if not item:
#         return jsonify({"message": "Item not found"}), 404

#     db.session.delete(item)
#     db.session.commit()
#     return jsonify({"message": "Item deleted"}), 200


@bp.route("/removewishlist", methods=["POST"],endpoint="remove_wishlist_item")
@token_required
def remove_wishlist_item():
    auth_header = request.headers.get('Authorization')
    payload=auth_header.split(" ")[1]
    token = jwt.decode(payload, secret_key, algorithms=['HS256'])

    customer_id=token["id"]
    cs_id=customer_id

    data = request.get_json()
    vendor_service_id=data.get("vendor_service_id")
    if not vendor_service_id:
        return jsonify({"error":"vendor service id is required"}), 400
    
    wishlist_item = WishlistItem.query.filter_by(customer_id=cs_id, vendor_service_id=vendor_service_id).first()
    
    if wishlist_item:
        db.session.delete(wishlist_item)
        db.session.commit()
        vendor = VENDOR.query.get(vendor_service_id)
    if not vendor:
        return jsonify({"error": "Vendor not found"}), 404

    vendor_info = {
        "organization_name": vendor.organization_name,
        "person_name": vendor.person_name,
        "full_address": vendor.full_address,
        "email_id": vendor.email_id,
        "phone_no": vendor.phone_no,
        "service": vendor.service,
        "location": vendor.location,
        "gst_no": vendor.gst_no
        }
        
    return jsonify({"message": "removed to wishlist", "vendor": vendor_info}), 201


@bp.route("/allwishlist", methods=["GET"], endpoint="get_all_wishlist_items")
def get_all_wishlist_items():
    # Fetching all wishlist items from the database
    wishlist_items = WishlistItem.query.all()

    if not wishlist_items:
        return jsonify({"message": "Wishlist is empty"}), 404

    # Collecting vendor and customer information for each wishlist item
    all_wishlist_info = []
    for item in wishlist_items:
        vendor = VENDOR.query.get(item.vendor_service_id)
        user = User.query.get(item.customer_id)
        if vendor and user:
            ratings = Rating.query.filter_by(vendor_id=vendor.id).all()
        total_rating = 0
        count = 0
        for r in ratings:
            total_rating += r.rating
            count += 1
        
        average_rating = total_rating / count if count > 0 else 0

        wishlist_info = {
                "customer_id": item.customer_id,
                "customer_name": user.name,  # Assuming the User model has a 'name' field
                "vendor_service_id": item.vendor_service_id,
                "organization_name": vendor.organization_name,
                "person_name": vendor.person_name,
                "full_address": vendor.full_address,
                "email_id": vendor.email_id,
                "phone_no": vendor.phone_no,
                "service": vendor.service,
                "location": vendor.location,
                "gst_no": vendor.gst_no,
                "rating":average_rating

            }
        all_wishlist_info.append(wishlist_info)

    return jsonify({"wishlist": all_wishlist_info}), 200
    