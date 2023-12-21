# reminds me of CS50p, when i had to calculate a similar coin value, defining
# dollars, cents, quarters, dimes, nickles & pennies lol
# also, by checking other people's works, i can assure you that this code is
# almost the same for everybody, i doubt i did anything new or original

def main():
    dollars = get_input()
    cents = dollars * 100

    quarters = calculate_quarters(cents)
    cents = cents - quarters * 25

    dimes = calculate_dimes(cents)
    cents = cents - dimes * 10

    nickels = calculate_nickels(cents)
    cents = cents - nickels * 5

    pennies = calculate_pennies(cents)
    cents = cents - pennies

    coins = int(quarters + dimes + nickels + pennies)
    print(coins)


def get_input():
    while True:
        try:
            dollars = float(input("Change owed: "))

            if dollars > 0:
                return dollars

        except ValueError as error:
            print(error)
            print("Enter a valid ammount.")


def calculate_quarters(cents):
    quarters = cents // 25
    return quarters


def calculate_dimes(cents):
    dimes = cents // 10
    return dimes


def calculate_nickels(cents):
    nickels = cents // 5
    return nickels


def calculate_pennies(cents):
    pennies = cents
    return pennies


if __name__ == "__main__":
    main()
