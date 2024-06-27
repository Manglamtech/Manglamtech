from database.database import db
from sqlalchemy.exc import IntegrityError


class Currentbooking(db.Model):

    customer_id = db.Column(db.BigInteger(),primary_key=True)
    vendor_id = db.Column(db.BigInteger(),primary_key=True)
    current_booking= db.Column(db.String(50),nullable=False)
    booking_number = db.Column(db.String(50),unique=True)
    date_booking = db.Column(db.String(60) , nullable=False)
    date_event = db.Column(db.String(60), nullable=False)

    def __init__(self,customer_id,vendor_id,current_booking,booking_number,date_booking,date_event):
        self.customer_id=customer_id,
        self.vendor_id=vendor_id,
        self.current_booking=current_booking,
        self.booking_number=booking_number,
        self.date_booking=date_booking,
        self.date_event=date_event

    def to_dict(self):
        return {
            "customer_id":self.customer_id,
            "vendor_id":self.vendor_id,
            "current_booking":self.current_booking,
            "booking_number":self.booking_number,
            "date_booking":self.date_booking,
            "date_event":self.date_event
        }



