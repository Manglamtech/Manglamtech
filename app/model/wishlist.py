from database.database import db
from sqlalchemy.exc import IntegrityError



class WishlistItem(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    event = db.Column(db.String(80), nullable=False)
    item = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.BigInteger, default=1)
    created_at = db.Column(db.String(50))


    def __init__(self,id,event,item,quantity,created_at):
        self.id = id,
        self.event = event,
        self.item = item,
        self.quantity = quantity,
        self.created_at = created_at

    def to_dict(self):
        return {
            "id":self.id,
            "event":self.event,
            "item":self.item,
            "quantity":self.quantity,
            "created_at":self.created_at

        }