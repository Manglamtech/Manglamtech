from flask import Flask
from flask import Flask, Blueprint
from database.database import db
from app.customer import bp as customer_bp
from app.vendor import bp as vendor_bp
from app.event import bp as event_bp
from app.booking import bp as booking_bp
from app.auth import bp as auth_bp
from app.currentbooking import bp as currentbooking_bp
from app.wishlist import bp as wishlist_bp

app =  Flask(__name__)
app.secret_key = "your_secret_key"

def create_app():
    app.config["SQLALCHEMY_DATABASE_URI"]= "postgresql://postgres:shivanichauhan@localhost:5000/app"

    # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
    db.init_app(app)
    with app.app_context():
        db.create_all()


    app.register_blueprint(customer_bp,url_prefix="/customer")
    
    app.register_blueprint(vendor_bp,url_prefix="/vendor")

    app.register_blueprint(event_bp,url_prefix="/event")

    app.register_blueprint(booking_bp,url_prefix="/booking")

    app.register_blueprint(auth_bp)

    app.register_blueprint(currentbooking_bp)

    app.register_blueprint(wishlist_bp)




if __name__ == '__main__':
    create_app()
    app.run(debug=True,port =5001)