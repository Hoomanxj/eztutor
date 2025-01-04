#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <cs50.h>



int main(void)
{
    char *word = get_string("Please enter a word: \n");
    // TODO: Improve this hash function
    const int two_digit = 9;
    int l1 = toupper(word[0]) - 'A';
    int l2 = toupper(word[1]) - 'A';
    int l3 = toupper(word[2]) - 'A';

    printf("L1: %c, value: %i\n", word[0], l1);
    printf("L2: %c, value: %i\n", word[1], l2);
    printf("L3: %c, value: %i\n", word[2], l3);

    if (l1 >= two_digit && l2 >= two_digit)
    {
        l2 = l2 * 100;
        l3 = l3 * 10000;
    }
    else if (l1 >= two_digit && l2 < two_digit)
    {
        l2 = l2 * 100;
        l3 = l3 * 1000;
    }
    else if (l1 < two_digit && l2 >= two_digit)
    {
        l2 = l2 * 10;
        l3 = l3 * 1000;
    }
    else if (l1 < two_digit && l2 < two_digit)
    {
        l2 = l2 * 10;
        l3 = l3 * 100;
    }
    printf("L1: %c, value: %i\n", word[0], l1);
    printf("L2: %c, value: %i\n", word[1], l2);
    printf("L3: %c, value: %i\n", word[2], l3);
    printf("Hash number for %s, is: %i\n", word, (l3 + l2 + l1));
}
