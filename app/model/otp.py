from database.database import db
from sqlalchemy.exc import IntegrityError
import datetime

class OTP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # email_id = db.Column(db.String(100), nullable=False)
    phone_no = db.Column(db.String(20), nullable=False)
    otp = db.Column(db.BigInteger, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)