
from cli_api import call_api, print_item, print_product


def view_all():
    items, error = call_api("GET", "/inventory")
    if error:
        print("Error:", error)
        return
    if len(items) == 0:
        print("The inventory is empty.")
    for item in items:
        print(item["id"], "-", item["product_name"], "| $", item["price"], "| stock:", item["quantity"])


def view_one(item_id):
    item, error = call_api("GET", "/inventory/" + str(item_id))
    if error:
        print("Error:", error)
        return
    print_item(item)


def find_by_barcode(barcode):
    product, error = call_api("GET", "/search/barcode/" + barcode)
    if error:
        print("Error:", error)
        return
    print_product(product)


def find_by_name(name):
    results, error = call_api("GET", "/search", params={"name": name})
    if error:
        print("Error:", error)
        return
    if len(results) == 0:
        print("No products found.")
    for product in results:
        print_product(product)
        print("-----")
