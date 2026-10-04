
STARTING_ITEMS = [
    {
        "id": 1,
        "barcode": "0000000000001",
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar, sea salt",
        "price": 3.99,
        "quantity": 25,
    },
    {
        "id": 2,
        "barcode": "3017620422003",
        "product_name": "Nutella",
        "brands": "Ferrero",
        "ingredients_text": "Sugar, palm oil, hazelnuts, cocoa, skim milk powder",
        "price": 4.49,
        "quantity": 40,
    },
    {
        "id": 3,
        "barcode": "5449000000996",
        "product_name": "Coca-Cola",
        "brands": "Coca-Cola",
        "ingredients_text": "Carbonated water, sugar, caramel colour, phosphoric acid",
        "price": 1.50,
        "quantity": 100,
    },
]

inventory = []


def reset_inventory():
    # Put the starting items back (the tests use this)
    inventory.clear()
    for item in STARTING_ITEMS:
        inventory.append(dict(item))


reset_inventory()


def find_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return item
    return None


def find_by_barcode(barcode):
    if barcode == "":
        return None
    for item in inventory:
        if item["barcode"] == barcode:
            return item
    return None


def get_next_id():
    if len(inventory) == 0:
        return 1
    biggest = 0
    for item in inventory:
        if item["id"] > biggest:
            biggest = item["id"]
    return biggest + 1
