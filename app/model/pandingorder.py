from database.database import db
from sqlalchemy.exc import IntegrityError

class Pendingorder(db.Model):
    id=db.Column(db.BigInteger(),primary_key=True)
    event_type=db.Column(db.String(50))
    address=db.Column(db.String(50))
    enter_preferences=db.Column(db.String(50))
    phone_no=db.Column(db.BigInteger())
    city=db.Column(db.String(50))
    date=db.Column(db.String(60))
    time=db.Column(db.String(60))
    customer_id=db.Column(db.BigInteger())
    status = db.Column(db.Boolean)

    def to_dict(self):
        return{
            "id":self.id,
            "event_type":self.event_type,
            "address":self.address,
            "enter_preferences":self.enter_preferences,
            "phone_no":self.phone_no,
            "city":self.city,
            " date":self.date,
            "time":self.time,
            "customer_id":self.customer_id,
            "status": self.status


        }

    

