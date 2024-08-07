from database.database import db
from sqlalchemy.exc import IntegrityError


class Feedbox(db.Model):
    id = db.Column(db.BigInteger(), primary_key=True)
    name = db.Column(db.String(100))
    email_id = db.Column(db.String(100), unique=True)
    events = db.Column(db.String(100))

    @staticmethod
    def create_feedbox(name, email_id, events):
        new_feedbox = Feedbox(name=name, email_id=email_id, events=events)
        db.session.add(new_feedbox)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return None
        return new_feedbox

