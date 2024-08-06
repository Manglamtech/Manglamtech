from database.database import db
from sqlalchemy.exc import IntegrityError

class VENDOR(db.Model):
    id=db.Column(db.BigInteger(),primary_key=True)
    organization_name=db.Column(db.String(50))
    person_name=db.Column(db.String(50))
    full_address=db.Column(db.String(50))
    email_id=db.Column(db.String(50),unique=True)
    password=db.Column(db.Unicode())
    phone_no=db.Column(db.BigInteger())
    service=db.Column(db.String(50))
    location=db.Column(db.String(50))
    gst_no=db.Column(db.String(50))
    district=db.Column(db.String(50))
    state=db.Column(db.String(50))
    
    # events= db.relationship("EVENT",backref="vendor",lazy=True,)
    bookings = db.relationship("Booking",backref="vendor",lazy=True,)
    rating=db.relationship("Rating",backref="vendor",lazy=True,)
    wishlist=db.relationship("WishlistItem",backref="vendor",lazy=True)
    

    def __init__(self,organization_name,person_name,full_address,email_id,password,phone_no,service,location,gst_no,district,state):
        self.organization_name=organization_name,
        self.person_name=person_name,
        self.full_address=full_address,
        self.email_id=email_id,
        self.password=password,
        self.phone_no=phone_no,
        self.service=service,
        self.location=location,
        self.gst_no=gst_no,
        self.district=district,
        self.state=state

    @staticmethod
    def create_vendor(payload):
        gst_no = payload["gst_no"]
        if gst_no == 0:
            gst_no = None

        vendor=VENDOR(
            organization_name=payload["organization_name"],
            person_name=payload["person_name"],
            full_address=payload["full_address"],
            email_id=payload["email_id"],
            password=payload["password"],
            phone_no=payload["phone_no"],
            service=payload["service"],
            location=payload["location"],
            gst_no=payload["gst_no"],
            district=payload["district"],
            state=payload["state"]

        )

        try:
            db.session.add(vendor)
            db.session.commit()
            return True
        except IntegrityError:
            return False

