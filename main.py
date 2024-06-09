from flask import Flask,request,jsonify,session
from database.database import db
from model.customer import User
from model.vendor import VENDOR
from model.event import EVENT
import datetime
import bcrypt
import json
import jwt



app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['secret_key'] = "this is secret"


def token_required(f):
    def decorated(*args, **kwargs):
        # token = request.args.get('token')
        token = request.headers['Authorization'].split()[1]
        if not token:
            return jsonify({'error': 'token is missing'}), 403
        try:
            jwt.decode(token, app.config['secret_key'], algorithms="HS256")
        except Exception as error:
            return jsonify({'error': 'token is invalid/expired'})
        return f(*args, **kwargs)
    return decorated
 

def create_app():
    app.config["SQLALCHEMY_DATABASE_URI"]= "postgresql://postgres:shivanichauhan@localhost:5000/app"
    # app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///user.db"
    db.init_app(app)
    with app.app_context():
        db.create_all()




# registration form
@app.route("/customer/registration",methods=["POST"])
def registration():
    current_date=str(datetime.datetime.now())
    data=request.get_json()
    if data:
        customer_id=data.get("customer_id")
        name=data.get("name")
        email_id=data.get("email_id")
        phone_no=data.get("phone_no")
        full_address=data.get("full_address")
        event=data.get("event")
        password=data.get("password")
        created_at=current_date
        lastupdated=current_date
        print(customer_id,name,email_id,phone_no,full_address,event,password,created_at,lastupdated)
        
        
        
        
        if customer_id and name and email_id and phone_no and full_address and event and password :
            existing_user= User.query.filter_by(email_id=email_id).first()
            if existing_user:
                return jsonify({"message": "User already exists"}), 400
            else:
                hashed_password= bcrypt.hashpw(
                    password.encode("utf-8","ignore"),bcrypt.gensalt()
                )

                if User.create_user(
                    {
                        "customer_id":customer_id,
                        "name":name,
                        "email_id":email_id,
                        "phone_no":phone_no,
                        "full_address":full_address,
                        "event":event,
                        "password":hashed_password,
                        "created_at":created_at,
                        "lastupdated":lastupdated,
                    }
                ):

                    return jsonify({"message": "User created successfully"}), 201
                else:
                    return jsonify({"message": "Failed to create user"}), 500
        else:
            return jsonify({"message": "Missing fields"}), 400
    else:
        return jsonify({"message": "No data provided"}), 400
            
@app.route("/users",methods=["GET"])
def get_users():
    users =User.query.all()
    result=[]
    for user in users:
        user_data={
            "customer_id":user.customer_id,
            "name":user.name,
            "email_id":user.email_id,
            "phone_no":user.phone_no,
            "full_address":user.full_address,
            "event":user.event,
            # "password":user.password,
            "created_at":user.created_at,
            "lastupdated":user.lastupdated
        }

        result.append(user_data)
    print(result)
    return jsonify(result), 200


@app.route("/users/<customer_id>", methods=["GET"])
def get_user_by_id(customer_id):

    user= User.query.filter_by(customer_id=customer_id).first()
    if user:
        user_data={
            "customer_id": user.customer_id,
            "name": user.name,
            "email_id": user.email_id,
            "phone_no": user.phone_no,
            "full_address": user.full_address,
            "event": user.event,
            # "password":user.password,
            "created_at":user.created_at,
            "lastupdated":user.lastupdated
        }

        return jsonify(user_data), 200
    else:
        return jsonify({"message": "User not found"}), 404
    
@app.route("/users/<customer_id>", methods=["PUT"])
def update_user(customer_id):
    current_date=str(datetime.datetime.now())

    data=request.get_json()
    user= User.query.filter_by(customer_id=customer_id).first()
    if user:
        user.name = data.get("name", user.name)
        user.email_id = data.get("email_id", user.email_id)
        user.phone_no = data.get("phone_no", user.phone_no)
        user.full_address = data.get("full_address", user.full_address)
        user.event = data.get("event", user.event)
        # user.password=data.get("password",user.password)
        user.lastupdated=current_date

        try:
            db.session.commit()
            return jsonify({"message": "User updated successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Failed to update user"}), 500
    else:
        return jsonify({"message": "User not found"}), 404

@app.route("/users/<customer_id>",methods=["DELETE"])
def user_delete(customer_id):
    user = User.query.filter_by(customer_id=customer_id).first()
    if user:
        try:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "User deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Failed to delete user"}), 500
    else:
        return jsonify({"message": "User not found"}), 404
    

# authentication logic
@app.route("/logging",methods=["POST"])
def logging():
    data=request.get_json()
    if data:
        email_id=data.get("email_id")
        password=data.get("password")
        print(email_id,password)
        if email_id and password:
            # Retrieve user from the database by email
            user=User.query.filter_by(email_id=email_id).first()
            if user:
                # Check if the provided password matches the hashed password stored in the database
                if bcrypt.checkpw(password.encode("utf-8"), user.password):
                    token = jwt.encode({'user': user.email_id, 'exp': datetime.datetime.utcnow(
                ) + datetime.timedelta(seconds=120)}, app.config['secret_key'])
                    # return jsonify(token)
                    return jsonify({"message": "Login successful"}), 200
                else:
                    return jsonify({"message": "Invalid email or password"}), 401
            else:
                return jsonify({"message": "Missing email or password"}), 400
        else:
            return jsonify({"message": "No data provided"}), 400
        

@app.route("/update_password",methods=["POST"])
@token_required
def update_password():
    data= request.get_json()
    if data:
        customer_id=data.get("customer_id")
        email_id=data.get("email_id")
        old_password=data.get("old_password")
        new_password=data.get("new_password")
        if customer_id and email_id and old_password and new_password:
            user=User.query.filter_by(email_id=email_id).first()
            if user:
                if bcrypt.checkpw(old_password.encode("utf-8"),user.password):
                    hashed_new_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
                    user.password = hashed_new_password
                    db.session.commit()

                    return jsonify({"message": "Password updated successfully"}), 200
                else:
                    return jsonify({"message": "Invalid old password"}), 401
            else:
                return jsonify({"message": "User not found"}), 404
        else:
            return jsonify({"message": "Missing data"}), 400
    else:
        return jsonify({"message": "No data provided"}), 400


# logoutendpoint
@app.route("/logout",methods=["POST"])
def logout():
    session.clear()
    return jsonify("you are out of the application")


# for vender registrstion

@app.route("/vendor/registration",methods=["POST"])
def vendor_registration():
    data= request.get_json()
    if data:
        vendor_id=data.get("vendor_id")
        organization_name=data.get("organization_name")
        person_name=data.get("person_name")
        full_address=data.get("full_address")
        email_id=data.get("email_id")
        password=data.get("password")
        phone_no=data.get("phone_no")
        event=data.get("event")
        gst_no=data.get("gst_no")
        print(vendor_id,organization_name,person_name,full_address,email_id,phone_no,event,gst_no)

        if vendor_id and organization_name and person_name and full_address and email_id and password and phone_no and event and gst_no:
            existing_user= VENDOR.query.filter_by(email_id=email_id).first()
            if existing_user:
                return jsonify({"message": "User already exists"}), 400
            else:
                hashed_password= bcrypt.hashpw(
                    password.encode("utf-8","ignore"),bcrypt.gensalt()
                )

            
                if VENDOR.create_vendor(
                        {
                        "vendor_id":vendor_id,
                        "organization_name":organization_name,
                        "person_name":person_name,
                        "full_address":full_address,
                        "email_id":email_id,
                        "password":hashed_password,
                        "phone_no":phone_no,
                        "event":event,
                        "gst_no":gst_no
                    }
                ):
                    return jsonify({"message": "User created successfully"}), 201
                else:
                    return jsonify({"message": "Failed to create user"}), 500
        else:
            return jsonify({"message": "Missing fields"}), 400
    else:
        return jsonify({"message": "No data provided"}), 400 

@app.route("/vendors",methods=["GET"])
def get_vendor():
    vendors=VENDOR.query.all()
    result=[]
    for vendor in vendors:
        vendor_data={
            "vendor_id":vendor.vendor_id,
            "organization_name":vendor.organization_name,
            "person_name":vendor.person_name,
            "full_address":vendor.full_address,
            "email_id":vendor.email_id,
            "phone_no":vendor.phone_no,
            "event":vendor.event,
            "gst_no":vendor.gst_no
        }

        result.append(vendor_data)
    return jsonify(result), 200

@app.route("/vendors/<vendor_id>",methods=["GET"])
def get_vendor_by_id(vendor_id):
    vendor = VENDOR.query.filter_by(vendor_id=vendor_id).first()
    if vendor:
        vendor_data={
            "vendor_id":vendor.vendor_id,
            "organization_name":vendor.organization_name,
            "person_name":vendor.person_name,
            "full_address":vendor.full_address,
            "email_id":vendor.email_id,
            "phone_no":vendor.phone_no,
            "event":vendor.event,
            "gst_no":vendor.gst_no
        }

        return jsonify(vendor_data),200
    else:
        return jsonify({"message":"Vendor not found"}), 400

@app.route("/vendors/<vendor_id>",methods=["PUT"])
def update_vendor(vendor_id):
    data=request.get_json()
    vendor=VENDOR.query.filter_by(vendor_id=vendor_id).first()
    if vendor:
        vendor.organization_name=data.get("organization_name",vendor.organization_name)
        vendor.person_name=data.get("person_name",vendor.person_name)
        vendor.full_address=data.get("full_address",vendor.full_address)
        vendor.email_id=data.get("email_id",vendor.email_id)
        vendor.phone_no=data.get("phone_no",vendor.phone_no)
        vendor.event=data.get("event",vendor.event)
        vendor.gst_no=data.get("gst_no",vendor.gst_no)

        try:
            db.session.commit()
            return jsonify({"message": "Vendor updated successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Failed to update vendor"}), 500
    else:
        return jsonify({"message": "Vendor not found"}), 404
    
@app.route("/vendors/<vendor_id>",methods=["DELETE"])
def vender_delete(vendor_id):
    vendor=VENDOR.query.filter_by(vendor_id=vendor_id).first()
    if vendor:
        try:
            db.session.delete(vendor)
            db.session.commit()
            return jsonify({"message":"Vendor deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message":"Failed to delete vendor"}), 500
    else:
        return jsonify({"message":"Vendor not found"}), 404

# vendor_authentication
@app.route("/vendors/logging",methods=["POST"])
def vender_logging():
    data=request.get_json()
    if data:
        email_id=data.get("email_id")
        password=data.get("password")
        if email_id and password:
            vendor=VENDOR.query.filter_by(email_id=email_id).first()
            if vendor:
                if bcrypt.checkpw(password.encode("utf--8"),vendor.password):
                    return jsonify({"message":"Login successful"}), 200
                else:
                    return jsonify({"message":"Invalid email or password"}), 401
            else:
                return jsonify({"message":"Missing email or password"}), 400
        else:
            return jsonify({"message":"No data provided"}), 400
        
@app.route("/vendor/update_password",methods=["POST"])
def vendor_update_password():
    data=request.get_json()
    if data:
        vendor_id=data.get("vendor_id")
        email_id=data.get("email_id")
        old_password=data.get("password")
        new_password=data.get("new_password")
        if vendor_id and email_id and old_password and new_password:
            vendor=VENDOR.query.filter_by(email_id=email_id).first()
            if vendor:
                if bcrypt.checkpw(old_password.encode("utf-8"),vendor.password):
                    hashed_new_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt().decode("utf-8"))
                    vendor.password = hashed_new_password
                    db.session.commit()

                    return jsonify({"message": "Password updated successfully"}), 200
                else:
                    return({"message": "Invalid old password"}), 401
            else:
                return jsonify({"message": "Vendor not found"}), 404
        else:
            return jsonify({"message": "Missing data"}), 400
    else:
        return jsonify({"message": "No data provided"}), 400
    
# api for event

@app.route("/create/event",methods=["POST"])
def create_event():
    try:
        order_data = request.json
        print(order_data)
        entry = EVENT(**order_data)
        
        db.session.add(entry)
        db.session.commit()
   
        return jsonify(entry.to_dict()), 201
    except Exception as e:
        return jsonify({"status": "Failed", "message": str(e)}), 500

    
@app.route('/events', methods=['GET'])
def get_all_events():
    
    events = EVENT.query.all()
    output = []
    for event in events:
        event_data = {
            'event_code': event.event_code,
            'event': event.event,
            'customer_id': event.customer_id,
            # 'vendor_id': event.vendor_id,
            'booking_status': event.booking_status
        }
        output.append(event_data)
    return jsonify({'events': output})

@app.route('/events/<int:customer_id>', methods=['GET'])
def get_event(customer_id):
    event = EVENT.query.filter_by(customer_id=customer_id).first()
    if not event:
        return jsonify({'message': 'Event not found'}), 404
    event_data = {
        'event_code': event.event_code,
        'event': event.event,
        'customer_id': event.customer_id,
        # 'vendor_id': event.vendor_id,
        'booking_status': event.booking_status
    }
    return jsonify({'event': event_data})

@app.route('/events/<int:customer_id>', methods=['PUT'])
def update_event(customer_id):
    data = request.get_json()
    event = EVENT.query.filter_by(customer_id=customer_id).first()
    if not event:
        return jsonify({'message': 'Event not found'}), 404
    event.event_code = data['event_code']
    event.event = data['event']
    event.customer_id = data['customer_id']
    # event.vendor_id = data['vendor_id']
    event.booking_status = data['booking_status']
    db.session.commit()
    return jsonify({'message': 'Event updated successfully'})

@app.route('/events/<int:customer_id>', methods=['DELETE'])
def delete_event(customer_id):
    event = EVENT.query.filter_by(customer_id=customer_id).first()
    if not event:
        return jsonify({'message': 'Event not found'}), 404
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted successfully'})







        
if __name__ =="__main__":
    create_app()
    app.run(debug=True,port=5001)
