from app.model.wishlist import WishlistItem
from database.database import db
import datetime
from flask import request,jsonify
from . import bp



@bp.route("/wishlist", methods=["POST"])
def add_wishlist_item():
    current_date=str(datetime.datetime.now())
    data=request.get_json()

    item = WishlistItem(
        id = data.get("id"),
        event=data.get("event"),
        item=data.get("item"),
        quantity=data.get("quantity", 1),
        created_at=current_date

        
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201

@bp.route("/wishlist/<event>",methods=["GET"])
def get_wishlist(event):
    items = WishlistItem.query.filter_by(event=event).all()
    result = [{"id": item.id, "event": item.event, "item": item.item, "quantity": item.quantity, "created_at": item.created_at} for item in items]
    return jsonify(result), 200


@bp.route('/wishlist/<int:id>', methods=['DELETE'])
def delete_wishlist_item(id):
    item = WishlistItem.query.get(id)
    if not item:
        return jsonify({"message": "Item not found"}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted"}), 200
