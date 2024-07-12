from app.model.otp import OTP
from app.model.otp_email import OtpEmail
from database.database import db
from flask import request,jsonify
from . import bp
import random
import datetime
from twilio.rest import Client
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

TWILIO_ACCOUNT_SID = 'ACbe0b70cf33344d3820f09fde5c804338'
TWILIO_AUTH_TOKEN = '4908d1ad671401ee8e6894327339c036'
TWILIO_PHONE_NUMBER = '+19452371655'


def send_otp( phone_no):
    otp = random.randint(100000, 999999)
    new_otp = OTP( phone_no=phone_no, otp=otp)
    db.session.add(new_otp)
    db.session.commit()
    print(f"OTP for {phone_no} is {otp}")
    # client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    # message = client.messages.create(
    # from_='+19452371655',
    # body=f'Your OTP is {otp}',
    # to='+918630219379'
    # )
    # print(message.sid)
    return otp

def send_otp_email(email_id):
    otp = random.randint(100000, 999999)
    new_otp = OtpEmail( email_id=email_id, otp_email=otp)
    db.session.add(new_otp)
    db.session.commit()
    print(f"OTP for {email_id} is {otp}")

    
# Send OTP via Email using smtplib
    # msg = MIMEMultipart()
    # msg['From'] = EMAIL_FROM
    # msg['To'] = email_id
    # msg['Subject'] = EMAIL_SUBJECT
    # body = f"Your OTP code is {otp}"
    # msg.attach(MIMEText(body, 'plain'))

    # server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    # server.starttls()
    # server.login(SMTP_USERNAME, SMTP_PASSWORD)
    # text = msg.as_string()
    # server.sendmail(EMAIL_FROM, email_id, text)
    # server.quit()
    return otp

@bp.route("/send_otp_phone", methods=["POST"],endpoint="phone_otp")
def send_otp_endpoint():
    data = request.get_json()
    phone_no = data.get("phone_no")
    
    if phone_no:
        send_otp(phone_no)
        return jsonify({"message": "OTP sent successfully"}), 200
    else:
        return jsonify({"message": "Phone No are required"}), 400

@bp.route("/verify_otp_phone", methods=["POST"],endpoint="verify_phone")
def verify_otp():
    data = request.get_json()
    phone_no = data.get("phone_no")
    otp = data.get("otp")
    
    valid_otp = OTP.query.filter_by(phone_no=phone_no, otp=otp).first()
    if valid_otp:
        valid_time= datetime.datetime.utcnow() - valid_otp.created_at
        if valid_time.total_seconds() <= 120:  
            db.session.delete(valid_otp)
            db.session.commit()
            return jsonify({"message": "OTP verified successfully"}), 200
        else:
            return jsonify({"message": "OTP has expired"}), 400
    else:
        return jsonify({"message": "Invalid OTP"}), 400


@bp.route("/send_otp_email", methods=["POST"],endpoint="emailotp")
def send_otp_endpoint():
    data = request.get_json()
    email_id = data.get("email_id")
    
    if email_id:
        send_otp_email(email_id)
        return jsonify({"message": "OTP sent successfully"}), 200
    else:
        return jsonify({"message": "email_id is required"}), 400


@bp.route("/verify_email", methods=["POST"],endpoint="verify_email")
def verify_otp():
    data = request.get_json()
    email_id = data.get("phone_no")
    otp_email = data.get("otp_email")
    
    valid_otp = OtpEmail.query.filter_by(email_id=email_id, otp_email=otp_email).first()
    if valid_otp:
        valid_time= datetime.datetime.utcnow() - valid_otp.created_at
        if valid_time.total_seconds() <= 120:  

            db.session.delete(valid_otp)
            db.session.commit()
            return jsonify({"message": "OTP verified successfully"}), 200
        else:
            return jsonify({"message": "OTP has expired"}), 400
    else:
        return jsonify({"message": "Invalid OTP"}), 400
    



