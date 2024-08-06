from database.database import db
from sqlalchemy.exc import IntegrityError





class User(db.Model):
    id= db.Column(db.BigInteger(), primary_key=True)
    name=db.Column(db.String(100))
    email_id=db.Column(db.String(100),unique=True)
    phone_no=db.Column(db.BigInteger())
    full_address=db.Column(db.String(100))
    pincode=db.Column(db.BigInteger())
    password=db.Column(db.Unicode())
    district=db.Column(db.String(50))
    state=db.Column(db.String(50))
    created_at=db.Column(db.String(50))
    lastupdated=db.Column(db.String(50))
    # events= db.relationship("EVENT",backref="user",lazy=True)
    bookings= db.relationship("Booking",backref="user",lazy=True)
    rating=db.relationship("Rating",backref="user",lazy=True,)
    wishlist=db.relationship("WishlistItem",backref="user",lazy=True)

    
    def __init__(self,name,email_id,phone_no,full_address,pincode,password,district,state,created_at,lastupdated):
        self.name= name
        self.email_id= email_id
        self.phone_no= phone_no
        self.full_address= full_address
        self.pincode= pincode
        self.password= password
        self.district=district
        self.state=state
        self.created_at= created_at 
        self.lastupdated= lastupdated 

    def to_dict(self):
        return{
            "id":self.id,
            "name":self.name,
            "email_id":self.email_id,
            "phone_no":self.phone_no,
            "full_address":self.full_address,
            "pincode":self.pincode
        }

    @staticmethod
    def create_user(payload):
        user=User(
            name= payload["name"],
            email_id= payload["email_id"],
            phone_no= payload["phone_no"],
            full_address= payload["full_address"],
            pincode= payload["pincode"],
            password= payload["password"],
            district=payload["district"],
            state=payload["state"],
            created_at= payload["created_at"],
            lastupdated= payload["lastupdated"]
            
        )  

        try:
            db.session.add(user)
            db.session.commit() 
            return True
        except IntegrityError:
            return False
