#include <cs50.h>
#include <stdio.h>

int get_cents(void);
int calculate_quarters(int cents);
int calculate_dimes(int cents);
int calculate_nickels(int cents);
int calculate_pennies(int cents);

int main(void)
{
    int cents = get_cents();

    int quarters = calculate_quarters(cents);
    cents = cents - quarters * 25;

    int dimes = calculate_dimes(cents);
    cents = cents - dimes * 10;

    int nickels = calculate_nickels(cents);
    cents = cents - nickels * 5;

    int pennies = calculate_pennies(cents);
    cents = cents - pennies * 1;

    int coins = quarters + dimes + nickels + pennies;

    printf("%i\n", coins);
}

int get_cents(void)
{
    int cents;

    do
    {
        cents = get_int("Change Owed: ");
    }
    while (cents < 0);

    return cents;
}

/// tiny rant over here, a friend and i came up with the 'just divide cents by the value of the coin' for the code, straightforward,
/// practical, useful. However most people solve this exercise closer to this:
/// int quarters = 0
/// while (cents >= 25)
/// {
/// cents = cents - 25;
/// quarters++;
/// now, my question is, why? why would you do such a longer code and process
/// when you can just go 'haha 25 cents = one quarter' ??? am i missing something?

int calculate_quarters(int cents)
{
    int quarters = cents / 25;
    return quarters;
}

int calculate_dimes(int cents)
{
    int dimes = cents / 10;
    return dimes;
}

int calculate_nickels(int cents)
{
    int nickels = cents / 5;
    return nickels;
}

int calculate_pennies(int cents)
{
    int pennies = cents / 1;
    return pennies;
}