
from flask import Blueprint, jsonify, request
from database import inventory, find_item, find_by_barcode, get_next_id
from validation import check_numbers, check_new_item

crud = Blueprint("crud", __name__)


@crud.route("/inventory", methods=["GET"])
def get_all_items():
    return jsonify(inventory), 200


@crud.route("/inventory/<int:item_id>", methods=["GET"])
def get_one_item(item_id):
    item = find_item(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200


@crud.route("/inventory", methods=["POST"])
def add_item():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Please send JSON data"}), 400

    problem = check_new_item(data)
    if problem:
        return jsonify({"error": problem}), 400

    barcode = data.get("barcode", "")
    if find_by_barcode(barcode):
        return jsonify({"error": "That barcode is already in the inventory"}), 409
    new_item = {
        "id": get_next_id(),
        "barcode": barcode,
        "product_name": data["product_name"].strip(),
        "brands": data.get("brands", ""),
        "ingredients_text": data.get("ingredients_text", ""),
        "price": data["price"],
        "quantity": data["quantity"],
    }
    inventory.append(new_item)
    return jsonify(new_item), 201


@crud.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    item = find_item(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Please send JSON data"}), 400

    problem = check_numbers(data)
    if problem:
        return jsonify({"error": problem}), 400

    # only these fields are allowed to change
    allowed = ["product_name", "brands", "ingredients_text", "barcode", "price", "quantity"]
    changed = False
    for field in allowed:
        if field in data:
            item[field] = data[field]
            changed = True
    if not changed:
        return jsonify({"error": "No valid fields to update"}), 400
    return jsonify(item), 200


@crud.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = find_item(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    inventory.remove(item)
    return jsonify({"message": "Item deleted"}), 200
