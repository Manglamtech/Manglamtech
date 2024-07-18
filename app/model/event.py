from database.database import db
from sqlalchemy.exc import IntegrityError


class EVENT(db.Model):
    id=db.Column(db.BigInteger(),primary_key=True)
    event_code= db.Column(db.String(100))
    event= db.Column(db.String(100))
    # vendor_id= db.Column(db.BigInteger(),db.ForeignKey("vendor.id"))
    # customer_id= db.Column(db.BigInteger(), db.ForeignKey("user.id"))
    # booking_status= db.Column(db.Boolean,nullable=False)    

    
    
    def to_dict(self):
        return{
            "id":self.id,
            "event_code":self.event_code,
            "event":self.event,
            # "customer_id":self.customer_id,
            # "vendor_id":self.vendor_id,
            # "booking_ststus":self.booking_status
        }
    

