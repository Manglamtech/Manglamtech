from database.database import db
from sqlalchemy.exc import IntegrityError



class WishlistItem(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vendor_service_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False)


    def __init__(self,customer_id, vendor_service_id):
        self.customer_id = customer_id,
        self. vendor_service_id =  vendor_service_id,
        

    # def to_dict(self):
    #     return {
    #         "id":self.id,
    #         "customer_id":self.customer_id,
    #         "vendor_service_id,":self.vendor_service_id,

    #     }