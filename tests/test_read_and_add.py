# Tests for GET and POST on /inventory


# ----- GET -----

def test_get_all_items(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    assert len(response.get_json()) == 3


def test_get_one_item(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200
    assert response.get_json()["product_name"] == "Organic Almond Milk"


def test_get_item_not_found(client):
    response = client.get("/inventory/999")
    assert response.status_code == 404


# ----- POST -----

def test_add_item(client):
    new_item = {"product_name": "Oat Milk", "price": 3.5, "quantity": 12}
    response = client.post("/inventory", json=new_item)
    assert response.status_code == 201
    assert response.get_json()["id"] == 4
    assert len(client.get("/inventory").get_json()) == 4


def test_add_item_missing_fields(client):
    response = client.post("/inventory", json={"product_name": "Oat Milk"})
    assert response.status_code == 400


def test_add_item_bad_price(client):
    new_item = {"product_name": "Oat Milk", "price": -5, "quantity": 1}
    response = client.post("/inventory", json=new_item)
    assert response.status_code == 400


def test_add_item_no_json(client):
    response = client.post("/inventory", data="hello")
    assert response.status_code == 400


def test_add_item_duplicate_barcode(client):
    new_item = {"product_name": "Copy", "price": 1, "quantity": 1, "barcode": "3017620422003"}
    response = client.post("/inventory", json=new_item)
    assert response.status_code == 409
