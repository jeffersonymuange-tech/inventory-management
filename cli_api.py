
import requests

API_URL = "http://127.0.0.1:5000"


def call_api(method, path, **kwargs):

    
    try:
        response = requests.request(method, API_URL + path, timeout=15, **kwargs)
    except requests.RequestException:
        return None, "Could not connect to the API. Is the server running?"

    try:
        data = response.json()
    except ValueError:
        data = {}

    if response.status_code >= 400:
        return None, data.get("error", "Something went wrong")
    return data, None


def print_item(item):
    print("ID:          ", item["id"])
    print("Name:        ", item["product_name"])
    print("Brand:       ", item["brands"])
    print("Barcode:     ", item["barcode"])
    print("Price:       ", item["price"])
    print("Quantity:    ", item["quantity"])
    print("Ingredients: ", item["ingredients_text"])


def print_product(product):
    print("Name:        ", product["product_name"])
    print("Brand:       ", product["brands"])
    print("Barcode:     ", product["barcode"])
    print("Ingredients: ", product["ingredients_text"])
