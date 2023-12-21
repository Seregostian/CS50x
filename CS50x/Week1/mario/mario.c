#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;

    do
    {
        height = get_int("Height: ");

        if (height < 1 || height > 8)
        {
            /// If the user doesn’t, in fact, input a positive integer between 1 and 8, inclusive, when prompted, the program should
            /// re-prompt the user until they cooperate:
            printf("Height input is wrong, come on user, COOPERATE!\n");
        }
    }
    while (height < 1 || height > 8);
    /// Also, had to do a do-while to reprompt the user into COOPERATING!
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < height; j++)
        {
            if (j >= height - (i + 1))
            {
                printf("#");
            }
            else
            {
                printf(" ");
            }
        }
        printf("\n");
    }

    return 0;
}