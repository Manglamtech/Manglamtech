from database.database import db
from sqlalchemy.exc import IntegrityError


class Rating(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    vendor_id = db.Column(db.BigInteger, db.ForeignKey('vendor.id'), nullable=False)
    customer_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.BigInteger, nullable=False)

