


def ask_whole_number(question):
    while True:
        answer = input(question)
        try:
            return int(answer)
        except ValueError:
            print("Please type a whole number.")


def ask_price(question):
    while True:
        answer = input(question)
        try:
            return float(answer)
        except ValueError:
            print("Please type a number like 4.99")
