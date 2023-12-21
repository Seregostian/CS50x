#include <cs50.h>
#include <stdio.h>

// TODO: Prompt for start size

// TODO: Prompt for end size

// TODO: Calculate number of years until we reach threshold

// TODO: Print number of years

int main(void)
{
    int start, end;
    do
    {
        printf("Population Start Size: ");
        start = get_int("");
    }
    while (start < 9);

    do
    {
        printf("Population End Size: ");
        end = get_int("");
    }
    while (start > end);

    int current_size = start;
    int years_passed = 0;
    while (current_size < end)
    {
        current_size += current_size / 3 - current_size / 4;
        years_passed++;
    }

    printf("Years: %i\n", years_passed);
}