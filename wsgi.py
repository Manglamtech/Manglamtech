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
from app.verify_otp import bp as verify_otp_bp
from app.mehendiArtist import bp as mehandi_artist_bp
from app.tranportation import bp as transportation_bp
from app.event_organizer import bp as event_organizer_bp
from app.entertainment import bp as entertainment_bp
from app.themeAndDecor import bp as themeanddecore_bp
from app.digitai_service import bp as digitalservice_bp
from app.beautyArtisan import bp as beauty_artican_bp
from flask_cors import CORS
from app.image import bp as image_bp
from app.rating import bp as rating_bp
from app.foodandcatering import bp as foodcatering_bp
from app.venu_booking import bp as venu_bp

app =  Flask(__name__)
app.secret_key = "your_secret_key"
CORS(app)

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

    app.register_blueprint(verify_otp_bp)

    app.register_blueprint(mehandi_artist_bp)

    app.register_blueprint(transportation_bp)

    app.register_blueprint(event_organizer_bp)

    app.register_blueprint(entertainment_bp)

    app.register_blueprint(themeanddecore_bp)

    app.register_blueprint(digitalservice_bp)

    app.register_blueprint(beauty_artican_bp)

    app.register_blueprint(image_bp)
    
    app.register_blueprint(rating_bp)

    app.register_blueprint(foodcatering_bp)

    app.register_blueprint(venu_bp)
    


if __name__ == '__main__':
    create_app()
    app.run(debug=True,port =5001)