from database.database import db
from sqlalchemy.exc import IntegrityError


class Entertainment(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email_id=db.Column(db.String(50),unique=True)
    experience = db.Column(db.Integer, nullable=False)
    top_picks = db.Column(db.Boolean, default=False)
    price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    reviews = db.Column(db.Float, default=0.0)
    availability_status = db.Column(db.Boolean, nullable=False)

    # bookings = db.relationship("Booking",backref="entertainment",lazy=True,)

    def to_dict(self):
        return {
            "id":self.id,
            "name":self.name,
            "email_id":self.email_id,
            "experience":self.experience,
            "top_picks":self.top_picks,
            "price":self.price,
            "location":self.location,
            "reviews":self.reviews,
            "availability_status":self.availability_status
        }