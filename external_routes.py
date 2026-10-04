
from flask import Blueprint, jsonify, request
from database import inventory, find_by_barcode, get_next_id
from validation import check_numbers
from off_api import get_product_by_barcode, search_products, OpenFoodFactsError

external = Blueprint("external", __name__)


@external.route("/search/barcode/<barcode>", methods=["GET"])
def search_by_barcode(barcode):
    try:
        product = get_product_by_barcode(barcode)
    except OpenFoodFactsError as error:
        return jsonify({"error": str(error)}), 502
    if product is None:
        return jsonify({"error": "No product found for that barcode"}), 404
    return jsonify(product), 200


@external.route("/search", methods=["GET"])
def search_by_name():
    name = request.args.get("name", "").strip()
    if name == "":
        return jsonify({"error": "Please give a name to search for"}), 400
    try:
        results = search_products(name)
    except OpenFoodFactsError as error:
        return jsonify({"error": str(error)}), 502
    return jsonify(results), 200


@external.route("/inventory/import", methods=["POST"])
def import_item():
    # Gets a product from OpenFoodFacts and saves it in our inventory
    data = request.get_json(silent=True)
    if not data or not isinstance(data.get("barcode"), str) or data["barcode"].strip() == "":
        return jsonify({"error": "barcode is required"}), 400

    barcode = data["barcode"].strip()
    if find_by_barcode(barcode):
        return jsonify({"error": "That barcode is already in the inventory"}), 409

    problem = check_numbers(data)
    if problem:
        return jsonify({"error": problem}), 400

    try:
        product = get_product_by_barcode(barcode)
    except OpenFoodFactsError as error:
        return jsonify({"error": str(error)}), 502
    if product is None:
        return jsonify({"error": "No product found for that barcode"}), 404

    new_item = {
        "id": get_next_id(),
        "barcode": product["barcode"],
        "product_name": product["product_name"],
        "brands": product["brands"],
        "ingredients_text": product["ingredients_text"],
        "price": data.get("price", 0),
        "quantity": data.get("quantity", 0),
    }
    inventory.append(new_item)
    return jsonify(new_item), 201
