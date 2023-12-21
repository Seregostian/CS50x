#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
// Keep in mind:a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p,  q, r, s, t, u, v, w, x, y, z

int compute_score(string word);

int main(void)
{
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score1 < score2)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("It's been a tie!\n");
    }
    return 0;
}
/// https://www.ibm.com/docs/en/aix/7.1?topic=c-ctype-isalpha-isupper-islower-isdigit-isxdigit-isalnum-isspace-ispunct-isprint-isgraph-iscntrl-isascii-subroutines
/// i literally just googled useful ways to differentiate uppercase from lowercase and found an IBM article, so i went with
/// 'isupper/islower', very useful!

int compute_score(string word)
{
    int score = 0;
    for (int i = 0, len = strlen(word); i < len; i++)
    {
        char letter = word[i];
        if (isupper(letter))
        {
            score += POINTS[letter - 'A'];
        }
        else if (islower(letter))
        {
            score += POINTS[letter - 'a'];
        }
    }
    return score;
}