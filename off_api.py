
import requests

BASE_URL = "https://world.openfoodfacts.org"
HEADERS = {"User-Agent": "InventoryApp/1.0 (school project)"}


class OpenFoodFactsError(Exception):
    
    pass


def clean_product(product, barcode=""):
    
    return {
        "barcode": str(product.get("code") or barcode),
        "product_name": product.get("product_name") or "Unknown product",
        "brands": product.get("brands") or "",
        "ingredients_text": product.get("ingredients_text") or "",
    }


def get_product_by_barcode(barcode):
    
    url = BASE_URL + "/api/v2/product/" + barcode + ".json"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
    except requests.RequestException:
        raise OpenFoodFactsError("Could not connect to OpenFoodFacts")

    if response.status_code == 404:
        return None
    if response.status_code != 200:
        raise OpenFoodFactsError("OpenFoodFacts error: " + str(response.status_code))

    try:
        info = response.json()
    except ValueError:
        raise OpenFoodFactsError("OpenFoodFacts sent back bad data")

    
    if info.get("status") != 1:
        return None
    return clean_product(info["product"], barcode)


def search_products(name):
    
    url = BASE_URL + "/cgi/search.pl"
    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 5,
    }

    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=10)
    except requests.RequestException:
        raise OpenFoodFactsError("Could not connect to OpenFoodFacts")

    if response.status_code != 200:
        raise OpenFoodFactsError("OpenFoodFacts error: " + str(response.status_code))

    try:
        info = response.json()
    except ValueError:
        raise OpenFoodFactsError("OpenFoodFacts sent back bad data")

    results = []
    for product in info.get("products", []):
        results.append(clean_product(product))
    return results
