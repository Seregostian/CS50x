#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

unsigned int word_ammount;
unsigned int hash_val;

const unsigned int N = 9876;

node *table[N];

bool check(const char *word)
{
    int index = hash(word);

    node *cursor = table[index];

    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) != 0)
        {
            cursor = cursor->next;
        }
        else
        {
            return true;
        }
    }

    return false;
}

unsigned int hash(const char *word)
{
    unsigned long k = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        k += tolower(word[i]);
    }
    return k % N;
}

bool load(const char *dictionary)
{
    FILE *f = fopen(dictionary, "r");
    if (f == NULL)
    {
        return false;
    }
    char word[LENGTH + 1];
    while (fscanf(f, "%s", word) != EOF)
    {
        node *w = malloc(sizeof(node));
        if (w == NULL)
        {
            return false;
        }

        strcpy(w->word, word);
        hash_val = hash(word);
        w->next = table[hash_val];
        table[hash_val] = w;
        word_ammount++;
    }
    fclose(f);
    return true;
}
unsigned int size(void)
{
    return word_ammount;
}

bool unload(void)
{
    node *cursor = NULL;

    for (int i = 0; i < N; i++)
    {
        cursor = table[i];

        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;

            free(temp);
        }
    }

    return true;
}