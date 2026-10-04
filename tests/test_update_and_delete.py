# Tests for PATCH and DELETE on /inventory/<id>


# ----- PATCH -----

def test_update_item(client):
    response = client.patch("/inventory/2", json={"price": 5.25, "quantity": 7})
    assert response.status_code == 200
    data = response.get_json()
    assert data["price"] == 5.25
    assert data["quantity"] == 7
    assert data["product_name"] == "Nutella"  # this did not change


def test_update_item_not_found(client):
    response = client.patch("/inventory/999", json={"price": 1})
    assert response.status_code == 404


def test_update_item_bad_value(client):
    response = client.patch("/inventory/1", json={"price": "free"})
    assert response.status_code == 400


def test_update_item_nothing_to_change(client):
    response = client.patch("/inventory/1", json={"color": "red"})
    assert response.status_code == 400


# ----- DELETE -----

def test_delete_item(client):
    response = client.delete("/inventory/1")
    assert response.status_code == 200
    assert client.get("/inventory/1").status_code == 404
    assert len(client.get("/inventory").get_json()) == 2


def test_delete_item_not_found(client):
    response = client.delete("/inventory/999")
    assert response.status_code == 404
