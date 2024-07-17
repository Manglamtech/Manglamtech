from database.database import db
from sqlalchemy.exc import IntegrityError


class BeautyArtisan(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_information = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    top_picks = db.Column(db.Boolean, default=False)
    price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    reviews = db.Column(db.Float, default=0.0)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    availability_status = db.Column(db.Boolean, nullable=False)
    
    # bookings = db.relationship("Booking",backref="beauty_artisan",lazy=True,)


    def to_dict(self):
        return {
            "id":self.id,
            "name":self.name,
            "contact_information":self.contact_information,
            "experience":self.experience,
            "top_picks":self.top_picks,
            "price":self.price,
            "location":self.location,
            "reviews":self.reviews,
            'latitude': self.latitude,
            'longitude': self.longitude,
            "availability_status":self.availability_status
            
        }