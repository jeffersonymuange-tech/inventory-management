


def check_numbers(data):
    
    if "price" in data:
        price = data["price"]
        if isinstance(price, bool) or not isinstance(price, (int, float)) or price < 0:
            return "price must be a number that is 0 or more"
    if "quantity" in data:
        quantity = data["quantity"]
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 0:
            return "quantity must be a whole number that is 0 or more"
    return None


def check_new_item(data):
    
    for field in ["product_name", "price", "quantity"]:
        if field not in data:
            return field + " is required"

    name = data["product_name"]
    if not isinstance(name, str) or name.strip() == "":
        return "product_name must be some text"

    return check_numbers(data)
