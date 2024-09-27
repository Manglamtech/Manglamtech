from flask import Flask,request,jsonify,session
from database.database import db
from app.model.customer import User
from app.model.vendor import VENDOR
from app.model.otp import OTP
from app.model.otp_email import OtpEmail
from itsdangerous import URLSafeTimedSerializer
import jwt
import bcrypt
import datetime
from . import bp
from dotenv import load_dotenv
import os

load_dotenv()
secret_key = os.getenv("SECRET_KEYS")
# secret_key="this is secret"
app = Flask(__name__)
app.config['secret_key'] = secret_key
serializer = URLSafeTimedSerializer(app.config['secret_key'])

def token_required(f):
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        # print(auth_header)
        if auth_header:
            try:
                token = auth_header.split()[1]
            except IndexError:
                return jsonify({'error': 'Token format is invalid'}), 400
        else:
            return jsonify({'error':'Token is missing'}), 403

        try:
            jwt.decode(token, app.config['secret_key'], algorithms="HS256")
        except Exception as error:
           return jsonify({'error': 'token is invalid/expired'})
        return f(*args, **kwargs)

    return decorated


@bp.route("/logging",methods=["POST"])
def logging():
    data=request.get_json()
    if data:
        email_id=data.get("email_id")
        phone_no = data.get("phone_no")
        password=data.get("password")
        is_vendor=data.get("is_vendor")
        
        # print(email_id,password)
        if (email_id or phone_no) and password:
            user=None
            if is_vendor==True:
                if email_id:
                    user=VENDOR.query.filter_by(email_id=email_id).first()
                elif phone_no:
                    user = VENDOR.query.filter_by(phone_no=phone_no).first()

            else:
                if email_id:
                # Retrieve user from the database by email
                    user=User.query.filter_by(email_id=email_id).first()
                elif phone_no:
                    user = User.query.filter_by(phone_no=phone_no).first()
                
            if user:
                # Check if the provided password matches the hashed password stored in the database
                
                if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
                
                    token = jwt.encode({'user': user.email_id if email_id else user.phone_no,'id': user.id, 'exp': datetime.datetime.utcnow(
                ) + datetime.timedelta(seconds=3600)}, app.config['secret_key'])
                    return jsonify(token)
                    # return jsonify({"message": "Login successful"}), 200
                else:
                    return jsonify({"message": "Invalid email or password"}), 401
            else:
                return jsonify({"message": "Missing email or password"}), 400
        else:
            return jsonify({"message": "No data provided"}), 400
        
        
@bp.route("/vendor/update_password",methods=["POST"])
def vendor_update_password():
    data=request.get_json()
    if data:
        vendor_id=data.get("vendor_id")
        email_id=data.get("email_id")
        old_password=data.get("old_password")
        new_password=data.get("new_password")
        print(vendor_id,email_id,old_password,new_password)
        if vendor_id and email_id and old_password and new_password:
            vendor=VENDOR.query.filter_by(email_id=email_id).first()
            if vendor:
                hashed_password = bcrypt.hashpw(old_password.encode("utf-8"), bcrypt.gensalt())
                vendor.password = hashed_password
                if bcrypt.checkpw(old_password.encode("utf-8"),vendor.password):
                    hashed_new_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
                    vendor.password = hashed_new_password
                    db.session.commit()

                    return jsonify({"message": "Password updated successfully"}), 200
                else:
                    return({"message": "Invalid old password"}), 401
            else:
                return jsonify({"message": "Vendor not found"}), 404
        else:
            return jsonify({"message": "Missing data"}), 400
    else:
        return jsonify({"message": "No data provided"}), 400


@bp.route("/logout",methods=["POST"],endpoint="logout")
def logout():
    session.clear()
    return jsonify("you are out of the application")


@bp.route("/reset_password", methods=["POST"], endpoint="reset_password")

def reset_password():
    data = request.get_json()
    phone_no = data.get("phone_no")
    email_id = data.get("email_id")
    password = data.get("password")
    is_vendor=data.get("is_vendor")

    
    user = None
    if is_vendor==True:
        if phone_no:
            user = VENDOR.query.filter_by(phone_no=phone_no).first()
        elif email_id:
            user = VENDOR.query.filter_by(email_id=email_id).first()
    else:
        if email_id:
            # Retrieve user from the database by email
            user=User.query.filter_by(email_id=email_id).first()
        elif phone_no:
            user = User.query.filter_by(phone_no=phone_no).first()
                

    if user:
        hashed_password= bcrypt.hashpw(
                    password.encode("utf-8","ignore"),bcrypt.gensalt()
                ).decode("utf-8")

        # Update user's password
        user.password=hashed_password
        db.session.commit()
        return jsonify({"message": "Password reset successfully"}), 200
    else:
        return jsonify({"message": "User not found"}), 404




