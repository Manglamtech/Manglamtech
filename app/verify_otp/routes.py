from app.model.otp import OTP
from app.model.customer import User
from app.model.otp_email import OtpEmail
from database.database import db
from flask import request, jsonify
from . import bp
import random
import datetime                     
from twilio.rest import Client
import smtplib
from dotenv import load_dotenv
import os
# bockwoulheudgmij

load_dotenv()
# TWILIO_ACCOUNT_SID="AC"
# TWILIO_AUTH_TOKEN="2e"
def send_otp(phone_no):
    otp = random.randint(100000, 999999)
    new_otp = OTP(phone_no=phone_no, otp=otp)
    db.session.add(new_otp)
    db.session.commit()
    print(f"OTP for {phone_no} is {otp}")

    #     client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    #     # message = client.messages.create(
    #     # from_='+18509903829',
    #     # to='+9186302195677'
    #     # )

    #     # print(message.sid)
    #     message = client.messages.create(
    #     from_='+18509903829',
    #     body=f'Your OTP is {otp}',
    #     to='+9186302195677'
    #     )
    #     print(message.sid)
    return otp


def send_otp_email(email_id):
    otp = random.randint(100000, 999999)
    new_otp = OtpEmail(email_id=email_id, otp_email=otp)
    db.session.add(new_otp)
    db.session.commit()
    print(f"OTP for {email_id} is {otp}")
    sender_email_id = os.getenv("SENDER_ID")
    sender_password = os.getenv("SENDER_PASSWORD")  # Use an App Password if 2FA is enabled

    EMAIL_SUBJECT = "Subject: Your OTP for a Spectacular Event Journey Awaits!"

    # Email body
    body = f"""Dear Customer,

        Welcome to Manglam, your trusted partner for all things spectacular in events!
        To help you continue crafting unforgetable experiences, we need to verify your identity for a seamless journey.

        Your One-Time Password (OTP):
        [ {otp} ]

        This OTP is valid for the next 10 minutes, so let's get you back to planning your dream event!

        For your security, please do not share this OTP with anyone. Manglam takes your privacy and data security seriously, ensuring your event planning is as safe as it is exciting.

        If you didn't request this OTP, feel free to reach out to us at Vipin@manglam.com or contact our customer care at +91 9643169901.

        Looking forward to helping you create memories that last a lifetime!
        Best Regards,
        Team Manglam
        Your Partner in Every Event Dream
        www.manglam.tech"""
    
    msg = f"Subject: {EMAIL_SUBJECT}\n\n{body}"

    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login(sender_email_id, sender_password)
    s.sendmail(sender_email_id, email_id, msg)
    s.quit()

    return otp


@bp.route("/send_otp_phone", methods=["POST"], endpoint="phone_otp")
def send_otp_endpoint():
    data = request.get_json()
    phone_no = data.get("phone_no")

    if phone_no:
        send_otp(phone_no)
        return jsonify({"message": "OTP sent successfully"}), 200
    else:
        return jsonify({"message": "Phone No are required"}), 400


@bp.route("/verify_otp_phone", methods=["POST"], endpoint="verify_phone")
def verify_otp():
    data = request.get_json()
    phone_no = data.get("phone_no")
    otp = data.get("otp")

    valid_otp = OTP.query.filter_by(phone_no=phone_no, otp=otp).first()
    if valid_otp:
        valid_time = datetime.datetime.utcnow() - valid_otp.created_at
        if valid_time.total_seconds() <= 120:
            db.session.delete(valid_otp)
            db.session.commit()
            return jsonify({"message": "OTP verified successfully"}), 200
        else:
            return jsonify({"message": "OTP has expired"}), 400
    else:
        return jsonify({"message": "Invalid OTP"}), 400


@bp.route("/send_otp_email", methods=["POST"], endpoint="emailotp")
def send_otp_endpoint():
    data = request.get_json()
    email_id = data.get("email_id")

    if email_id:
        send_otp_email(email_id)
        return jsonify({"message": "OTP sent successfully"}), 200
    else:
        return jsonify({"message": "email_id is required"}), 400


@bp.route("/verify_email", methods=["POST"], endpoint="verify_email")
def verify_otp():
    data = request.get_json()
    email_id = data.get("email_id")
    otp_email = data.get("otp_email")

    valid_otp = OtpEmail.query.filter_by(email_id=email_id, otp_email=otp_email).first()
    if valid_otp:
        valid_time = datetime.datetime.utcnow() - valid_otp.created_at
        if valid_time.total_seconds() <= 120:

            db.session.delete(valid_otp)
            db.session.commit()
            return jsonify({"message": "OTP verified successfully"}), 200
        else:
            return jsonify({"message": "OTP has expired"}), 400
    else:
        return jsonify({"message": "Invalid OTP"}), 400


@bp.route("/otp_email", methods=["POST"], endpoint="email_otp")
def send_otp_endpoint():
    data = request.get_json()
    email_id = data.get("email_id")

    if not email_id:
        return jsonify({"message": "email_id is required"}), 400

    # Query the database to check if the email exists
    user = User.query.filter_by(email_id=email_id).first()

    if not user:
        return jsonify({"message": "Email does not exist in the database"}), 404

    send_otp_email(email_id)
    return jsonify({"message": "OTP sent successfully"}), 200
