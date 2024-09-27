from app.model.customer import User
from database.database import db
from flask import request,jsonify
import bcrypt
# from app.customer import Blueprint as bp
import datetime
from . import bp
from app.auth.routes import token_required,secret_key
import jwt


@bp.route("/registration",methods=["POST"],endpoint="customer_registration")
def registration():
    current_date=str(datetime.datetime.now())
    data=request.get_json()
    if data:
        name=data.get("name")
        phone_no=data.get("phone_no")
        email_id=data.get("email_id")
        full_address=data.get("full_address")
        pincode=data.get("pincode")
        password=data.get("password")
        district=data.get("district")
        state=data.get("state")
        created_at=current_date
        lastupdated=current_date
        print(name,email_id,phone_no,full_address,pincode,password,created_at,lastupdated)
        if  name and email_id and phone_no and full_address and pincode and password :
            existing_user= User.query.filter_by(email_id=email_id).first()
            if existing_user:
                return jsonify({"message": "User already exists"}), 400
            else:
                hashed_password= bcrypt.hashpw(
                    password.encode("utf-8","ignore"),bcrypt.gensalt(14)
                ).decode("utf-8")

                if User.create_user(
                    {
                        
                        "name":name,
                        "email_id":email_id,
                        "phone_no":phone_no,
                        "full_address":full_address,
                        "pincode":pincode,
                        "password":hashed_password,
                        "district":district,
                        "state":state,
                        "created_at":created_at,
                        "lastupdated":lastupdated,
                    }
                ):

                    return jsonify({"message": "User created successfully"}), 201
                else:
                    return jsonify({"message": "Failed to create user"}), 500
        else:
            return jsonify({"message": "Missing fields"}), 400
    else:
        return jsonify({"message": "No data provided"}),

@bp.route("/users",methods=["GET"], endpoint="get_users")
@token_required
def get_users():
    users =User.query.all()
    result=[]
    for user in users:
        user_data={
            "customer_id":user.id,
            "name":user.name,
            "email_id":user.email_id,
            "phone_no":user.phone_no,
            "full_address":user.full_address,
            "pincode":user.pincode,
            "district":user.district,
            "state":user.state,
            # "password":user.password,
            "created_at":user.created_at,
            "lastupdated":user.lastupdated
        }

        result.append(user_data)
    print(result)
    return jsonify(result), 200


@bp.route("/users/<customer_id>", methods=["GET"],endpoint="get_user_by_id")
@token_required

def get_user_by_id(customer_id):

    user= User.query.filter_by(id=customer_id).first()
    if user:
        user_data={
            "customer_id": user.id,
            "name": user.name,
            "email_id": user.email_id,
            "phone_no": user.phone_no,
            "full_address": user.full_address,
            "pincode": user.pincode,
            # "password":user.password,
            "created_at":user.created_at,
            "lastupdated":user.lastupdated
        }

        return jsonify(user_data), 200
    else:
        return jsonify({"message": "User not found"}), 404
    
@bp.route("/users/<customer_id>", methods=["PUT"],endpoint="update_user")
@token_required
def update_user(customer_id):
    current_date=str(datetime.datetime.now())

    data=request.get_json()
    user= User.query.filter_by(id=customer_id).first()
    if user:
        user.name = data.get("name", user.name)
        user.email_id = data.get("email_id", user.email_id)
        user.phone_no = data.get("phone_no", user.phone_no)
        user.full_address = data.get("full_address", user.full_address)
        user.pincode = data.get("pincode", user.pincode)
        # user.password=data.get("password",user.password)
        user.lastupdated=current_date

        try:
            db.session.commit()
            return jsonify({"message": "User updated successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Failed to update user"}), 500
    else:
        return jsonify({"message": "User not found"}), 404

@bp.route("/users/<customer_id>",methods=["DELETE"],endpoint="user_delete")
@token_required
def user_delete(customer_id):
    user = User.query.filter_by(id=customer_id).first()
    if user:
        try:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "User deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Failed to delete user"}), 500
    else:
        return jsonify({"message": "User not found"}), 404
    

@bp.route("/profile",methods=["GET"],endpoint="get_customer_profile")
@token_required
def get_customer_profile():
    auth_header = request.headers.get('Authorization')
    payload=auth_header.split(" ")[1]
    token = jwt.decode(payload, secret_key, algorithms=['HS256'])

    customer_id=token["id"]
    customer=User.query.get(customer_id)
    
    if customer:
        customer_data={
            "customer_id": customer.id,
            "name": customer.name,
            "email_id": customer.email_id,
            "phone_no": customer.phone_no,
            "full_address": customer.full_address,
            "pincode": customer.pincode,
            # "password":user.password,
            "created_at":customer.created_at,
            "lastupdated":customer.lastupdated
        }
        return jsonify(customer_data),200
    else:
        return jsonify({"message":"user not found"}), 400


@bp.route("/profile", methods=["PUT"], endpoint="edit_customer_profile")
@token_required
def edit_customer_profile():
    current_date=str(datetime.datetime.now())
    auth_header = request.headers.get('Authorization')
    payload = auth_header.split(" ")[1]
    token = jwt.decode(payload, secret_key, algorithms=['HS256'])

    customer_id = token["id"]
    user = User.query.get(customer_id)

    if user:
        data=request.get_json()
        if data.get("name") != "":
            user.name = data.get("name", user.name)
        if data.get("email_id") != "":
            user.email_id = data.get("email_id", user.email_id)
        if data.get("phone_no") != "":
            user.phone_no = data.get("phone_no", user.phone_no)
        if data.get("full_address") != "":
            user.full_address = data.get("full_address", user.full_address)
        if data.get("pincode") != "":
            user.pincode = data.get("pincode", user.pincode)
        if data.get("password") != "":
            password = data.get("password")
            hashed_password = bcrypt.hashpw(
                password.encode("utf-8", "ignore"),
                bcrypt.gensalt()
            ).decode("utf-8")
            user.password = hashed_password
        user.lastupdated=current_date
        try:
            db.session.commit()
            return jsonify({"message": "User updated successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Failed to update user"}), 500
    else:
        return jsonify({"message": "User not found"}), 404