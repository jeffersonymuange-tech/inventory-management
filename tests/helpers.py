# Fake data and a fake response shared by several test files.
from unittest.mock import Mock

# an item like the ones our API returns
ITEM = {
    "id": 1,
    "barcode": "123",
    "product_name": "Organic Almond Milk",
    "brands": "Silk",
    "ingredients_text": "Water, almonds",
    "price": 3.99,
    "quantity": 25,
}

# a product like the ones OpenFoodFacts returns
GOOD_DATA = {
    "status": 1,
    "product": {
        "code": "123",
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds",
    },
}

# a product after we cleaned it up
FAKE_PRODUCT = {
    "barcode": "111",
    "product_name": "Test Spread",
    "brands": "TestBrand",
    "ingredients_text": "Sugar, cocoa",
}


def make_response(status_code=200, data=None):
    # builds a fake response object
    response = Mock()
    response.status_code = status_code
    response.json.return_value = data
    return response
