
from cli_input import ask_whole_number, ask_price
from cli_view import view_all, view_one, find_by_barcode, find_by_name
from cli_change import add_item, update_item, delete_item, import_item


def show_menu():
    print()
    print("===== Inventory Menu =====")
    print("1. View all items")
    print("2. View one item")
    print("3. Add an item")
    print("4. Update price or stock")
    print("5. Delete an item")
    print("6. Find a product on OpenFoodFacts (barcode)")
    print("7. Find a product on OpenFoodFacts (name)")
    print("8. Import a product from OpenFoodFacts")
    print("0. Quit")


def main():
    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_all()
        elif choice == "2":
            view_one(ask_whole_number("Item ID: "))
        elif choice == "3":
            name = input("Product name: ")
            price = ask_price("Price: ")
            quantity = ask_whole_number("Quantity: ")
            brand = input("Brand (optional): ")
            barcode = input("Barcode (optional): ")
            add_item(name, price, quantity, brand, barcode)
        elif choice == "4":
            item_id = ask_whole_number("Item ID: ")
            price = ask_price("New price: ")
            quantity = ask_whole_number("New quantity: ")
            update_item(item_id, price, quantity)
        elif choice == "5":
            delete_item(ask_whole_number("Item ID: "))
        elif choice == "6":
            find_by_barcode(input("Barcode: ").strip())
        elif choice == "7":
            find_by_name(input("Product name: ").strip())
        elif choice == "8":
            barcode = input("Barcode: ").strip()
            price = ask_price("Price: ")
            quantity = ask_whole_number("Quantity: ")
            import_item(barcode, price, quantity)
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("That is not a valid option.")


if __name__ == "__main__":
    main()
