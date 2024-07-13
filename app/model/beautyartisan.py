from database.database import db
from sqlalchemy.exc import IntegrityError


class BeautyArtisan(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    top_picks = db.Column(db.Boolean, default=False)
    price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    reviews = db.Column(db.Float, default=0.0)
    distance = db.Column(db.Float, nullable=True)
    # bookings = db.relationship("Booking",backref="beauty_artisan",lazy=True,)


    def to_dict(self):
        return {
            "id":self.id,
            "name":self.name,
            "top_picks":self.top_picks,
            "price":self.price,
            "location":self.location,
            "reviews":self.reviews,
            "distance":self.distance
        }