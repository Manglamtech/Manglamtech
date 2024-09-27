from app.model.vendor import VENDOR
from database.database import db
from flask import request,jsonify
import bcrypt
from . import bp
from app.auth.routes import token_required,secret_key
from sqlalchemy.exc import IntegrityError
import jwt
from app.model.rating import Rating



@bp.route("/registration",methods=["POST"],endpoint="vendor_registration")

def vendor_registration():
    data= request.get_json()
    if data:
        
        organization_name=data.get("organization_name")
        person_name=data.get("person_name")
        full_address=data.get("full_address")
        email_id=data.get("email_id")
        password=data.get("password")
        phone_no=data.get("phone_no")
        service=data.get("service")
        location=data.get("location")
        gst_no=data.get("gst_no")
        district=data.get("district")
        state=data.get("state")

        print(type(id),type(organization_name),type(person_name),type(full_address),type(email_id),type(password),type(phone_no),type(gst_no))
        # print(vendor_id,organization_name,person_name,full_address,email_id,phone_no,event,gst_no)

        if organization_name and person_name and full_address and email_id and password and phone_no and service and location :
            existing_user= VENDOR.query.filter_by(email_id=email_id).first()
            if existing_user:
                return jsonify({"message": "User already exists"}), 400
            else:
                hashed_password= bcrypt.hashpw(
                    password.encode("utf-8","ignore"),bcrypt.gensalt()
                ).decode("utf-8")


            
                if VENDOR.create_vendor(
                        {
                        
                        "organization_name":organization_name,
                        "person_name":person_name,
                        "full_address":full_address,
                        "email_id":email_id,
                        "password":hashed_password,
                        "phone_no":phone_no,
                        "service":service,
                        "location":location,
                        "gst_no":gst_no,
                        "district":district,
                        "state":state

                    }
                ):
                    return jsonify({"message": "User created successfully"}), 201
                else:
                    return jsonify({"message": "Failed to create user"}), 500
        else:
            return jsonify({"message": "Missing fields"}), 400
    else:
        return jsonify({"message": "No data provided"}), 400 

@bp.route("/vendors",methods=["GET"],endpoint="get_vendors")
@token_required  
def get_vendor():
    vendors=VENDOR.query.all()
    result=[]
    for vendor in vendors:
        ratings = [ratings.rating for ratings in vendor.rating]
        average_rating = sum(ratings) / len(ratings) if ratings else 0
        
        vendor_data={
            "vendor_id":vendor.id,
            "organization_name":vendor.organization_name,
            "person_name":vendor.person_name,
            "full_address":vendor.full_address,
            "email_id":vendor.email_id,
            "phone_no":vendor.phone_no,
            "service":vendor.service,
            "location":vendor.location,
            "gst_no":vendor.gst_no,
            "district":vendor.district,
            "state":vendor.state,
            "ratings":average_rating
            # 'bookings': [{'id': booking.booking_id, 'name': booking.event_details} for booking in vendor.bookings]

        }

        result.append(vendor_data)
    return jsonify(result), 200

@bp.route("/vendors/<vendor_id>",methods=["GET"],endpoint="get_vendor_by_id")
@token_required
def get_vendor_by_id(vendor_id):
    vendor = VENDOR.query.get(vendor_id)
    if vendor:
        vendor_data={
            "vendor_id":vendor.id,
            "organization_name":vendor.organization_name,
            "person_name":vendor.person_name,
            "full_address":vendor.full_address,
            "email_id":vendor.email_id,
            "phone_no":vendor.phone_no,
            "service":vendor.service,
            "location":vendor.location,
            "gst_no":vendor.gst_no,
            # 'bookings': [{'id': booking.booking_id, 'name': booking.event_details} for booking in vendor.bookings],
            # 'rating': [{'id':rating.id, 'customer_id': rating.customer_id} for rating in vendor.rating]
        }

        return jsonify(vendor_data),200
    else:
        return jsonify({"message":"Vendor not found"}), 400

@bp.route("/vendors/<vendor_id>",methods=["PUT"],endpoint="update_vendor")
@token_required
def update_vendor(vendor_id):
    data=request.get_json()
    vendor=VENDOR.query.filter_by(id=vendor_id).first()
    if vendor:
        vendor.organization_name=data.get("organization_name",vendor.organization_name)
        vendor.person_name=data.get("person_name",vendor.person_name)
        vendor.full_address=data.get("full_address",vendor.full_address)
        vendor.email_id=data.get("email_id",vendor.email_id)
        vendor.phone_no=data.get("phone_no",vendor.phone_no)
        vendor.gst_no=data.get("gst_no",vendor.gst_no)

        try:
            db.session.commit()
            return jsonify({"message": "Vendor updated successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Failed to update vendor"}), 500
    else:
        return jsonify({"message": "Vendor not found"}), 404
    
@bp.route("/vendors/<vendor_id>",methods=["DELETE"],endpoint="delete_vendor")
@token_required
def vender_delete(vendor_id):
    vendor=VENDOR.query.filter_by(id=vendor_id).first()
    if vendor:
        try:
            db.session.delete(vendor)
            db.session.commit()
            return jsonify({"message":"Vendor deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message":"Failed to delete vendor"}), 500
    else:
        return jsonify({"message":"Vendor not found"}), 404



@bp.route('/set_vendor_credentials', methods=['POST'])
def set_vendor_credentials():
    data = request.get_json()

    email_id = data.get('email_id')
    new_username = data.get('person_name')
    new_password = data.get('password')

    if not email_id or not new_username or not new_password:
        print(email_id,new_username,new_password)
        return jsonify({"error": "Missing data"}), 400

    vendor = VENDOR.query.filter_by(email_id=email_id).first()

    if not vendor:
        return jsonify({"error": "Vendor not found"}), 404

    if VENDOR.query.filter_by(person_name=new_username).first():
        return jsonify({"error": "Username already taken"}), 409

    vendor.person_name = new_username
    vendor.password = bcrypt.hashpw(
                    new_password.encode("utf-8","ignore"),bcrypt.gensalt())
    
    try:
        db.session.commit()
        return jsonify({"message": "Username and password updated successfully"}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "An error occurred"}), 500
    
    
@bp.route("/vendorProfile",methods=["PUT"],endpoint="Edit_profile_data")
@token_required
def get_profile_data():
    auth_header = request.headers.get('Authorization')
    payload=auth_header.split(" ")[1]
        # print(payload)
    token = jwt.decode(payload, secret_key, algorithms=['HS256'])
        # print(token)
    vendor_id= token["id"]
    vendor=VENDOR.query.get(vendor_id)
    if vendor:
        data=request.get_json()
        if data.get("organization_name") != "":
            vendor.organization_name=data.get("organization_name",vendor.organization_name)
        if data.get("person_name") != "":
            vendor.person_name=data.get("person_name",vendor.person_name)
        if data.get("full_address") != "":
            vendor.full_address=data.get("full_address",vendor.full_address)
        if data.get("email_id") != "":
            vendor.email_id=data.get("email_id",vendor.email_id)
        if data.get("phone_no") != "":
            vendor.phone_no=data.get("phone_no",vendor.phone_no)
        if data.get("gst_no") != "":   
            vendor.gst_no=data.get("gst_no",vendor.gst_no)
        if data.get("password") != "":
            password = data.get("password")
            hashed_password = bcrypt.hashpw(
                password.encode("utf-8", "ignore"),
                bcrypt.gensalt()
            ).decode("utf-8")
            vendor.password = hashed_password
        
        try:
            db.session.commit()
            return jsonify({"message": "Vendor updated successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Failed to update vendor"}), 500
    else:
        return jsonify({"message": "Vendor not found"}), 404


@bp.route("/vendorProfile",methods=["GET"],endpoint="get_profile_data")
@token_required
def get_profile_data():
    auth_header = request.headers.get('Authorization')
    payload=auth_header.split(" ")[1]
        # print(payload)
    token = jwt.decode(payload, secret_key, algorithms=['HS256'])
        # print(token)
    vendor_id= token["id"]
    vendor=VENDOR.query.get(vendor_id)
    if vendor:
        vendor_data={
            "vendor_id":vendor.id,
            "organization_name":vendor.organization_name,
            "person_name":vendor.person_name,
            "full_address":vendor.full_address,
            "email_id":vendor.email_id,
            "phone_no":vendor.phone_no,
            "service":vendor.service,
            "location":vendor.location,
            "gst_no":vendor.gst_no,
        }
        return jsonify(vendor_data),200
    else:
        return jsonify({"message":"Vendor not found"}), 400



