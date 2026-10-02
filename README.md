# Inventory Management System

A Flask API and a menu-based command line app for managing store inventory.
It can also look up product details on the OpenFoodFacts website.
The inventory is a Python list, so it resets when the server restarts.

## Files

| File | What it does |
|------|--------------|
| app.py | Starts the Flask app |
| crud_routes.py | Add, view, update and delete routes |
| external_routes.py | OpenFoodFacts search and import routes |
| database.py | The inventory list and helper functions |
| validation.py | Checks the data people send |
| off_api.py | Calls the OpenFoodFacts API |
| cli.py | The menu program |
| cli_api.py, cli_view.py, cli_change.py, cli_input.py | Parts of the menu program |
| tests/ | Tests for everything above |

## Setup

```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run it

Terminal 1 starts the API (`python app.py`), terminal 2 starts the menu (`python cli.py`).

## API routes

| Method | Route | What it does |
|--------|-------|--------------|
| GET | /inventory | Get all items |
| GET | /inventory/<id> | Get one item |
| POST | /inventory | Add an item |
| PATCH | /inventory/<id> | Update an item |
| DELETE | /inventory/<id> | Delete an item |
| GET | /search/barcode/<barcode> | Find a product on OpenFoodFacts |
| GET | /search?name=milk | Search OpenFoodFacts by name |
| POST | /inventory/import | Get a product by barcode and add it |

Example item:

```json
{
  "id": 1,
  "barcode": "0000000000001",
  "product_name": "Organic Almond Milk",
  "brands": "Silk",
  "ingredients_text": "Filtered water, almonds, cane sugar, sea salt",
  "price": 3.99,
  "quantity": 25
}
```

Adding an item needs `product_name`, `price` and `quantity`.
Errors come back as JSON like `{"error": "Item not found"}`.
Status codes: 400 bad input, 404 not found, 409 duplicate barcode,
502 OpenFoodFacts problem.

Example with curl:

```bash
curl -X POST http://127.0.0.1:5000/inventory -H "Content-Type: application/json" -d '{"product_name": "Oat Milk", "price": 3.5, "quantity": 20}'
```

## Menu options

1 View all, 2 View one, 3 Add, 4 Update price or stock, 5 Delete,
6 Find on OpenFoodFacts (barcode), 7 Find on OpenFoodFacts (name),
8 Import from OpenFoodFacts, 0 Quit.

## Tests

Run `pytest`. The tests use `unittest.mock` to fake OpenFoodFacts and the API,
so they work without internet and without the server running.
