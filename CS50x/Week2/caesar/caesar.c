#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    {
        // found a stackoverflow article that gives this line as an answer, my approach was different, but i like this one better so
        // i kept it https://stackoverflow.com/questions/71361546/how-can-i-get-the-length-of-argv1
        for (int i = 0, len_argc = strlen(argv[1]); i < len_argc; i++)
        {
            char tmp = argv[1][i];
            if (!isdigit(tmp))
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }
    }
    int k = atoi(argv[1]);

    string plaintext = get_string("Plaintext: ");
    printf("Ciphertext: ");
    // Yet again, isupper and islower, as per the last code i used, that IBM article is sue useful
    for (int j = 0; j < strlen(plaintext); j++)
    {
        if (isupper(plaintext[j]))
        {
            printf("%c", (plaintext[j] - 'A' + k) % 26 + 'A');
        }
        else if (islower(plaintext[j]))
        {
            printf("%c", (plaintext[j] - 'a' + k) % 26 + 'a');
        }
        else
        {
            printf("%c", plaintext[j]);
        }
    }
    printf("\n");
}