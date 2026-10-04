
from cli_api import call_api, print_item


def add_item(name, price, quantity, brand="", barcode=""):
    data = {"product_name": name, "price": price, "quantity": quantity,
            "brands": brand, "barcode": barcode}
    item, error = call_api("POST", "/inventory", json=data)
    if error:
        print("Error:", error)
        return
    print("Item added!")
    print_item(item)


def update_item(item_id, price=None, quantity=None):
    data = {}
    if price is not None:
        data["price"] = price
    if quantity is not None:
        data["quantity"] = quantity
    if not data:
        print("Error: nothing to update")
        return
    item, error = call_api("PATCH", "/inventory/" + str(item_id), json=data)
    if error:
        print("Error:", error)
        return
    print("Item updated!")
    print_item(item)


def delete_item(item_id):
    result, error = call_api("DELETE", "/inventory/" + str(item_id))
    if error:
        print("Error:", error)
        return
    print(result["message"])


def import_item(barcode, price, quantity):
    item, error = call_api("POST", "/inventory/import",
                           json={"barcode": barcode, "price": price, "quantity": quantity})
    if error:
        print("Error:", error)
        return
    print("Imported and added to the inventory!")
    print_item(item)
