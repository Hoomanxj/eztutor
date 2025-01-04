#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void)
{
    // Store the alphabet in an array of characters
    char alphabet[26];
    int LEN_ALPHABET = 26;
    int PLAYER1_SCORE = 0;
    int PLAYER2_SCORE = 0;

    for (int i = 0; i < 26; i++)
    {
        alphabet[i] = i + 97; // Store 'a' to 'z'
    }

    // Store the Scrabble score values in another array
    int values[26] = {1, 3, 3, 2,  1, 4, 2, 4, 1, 8, 5, 1, 3,
                      1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

    // Get player answers
    string player1 = get_string("Player 1: \n");
    string player2 = get_string("Player 2: \n");

    int len1 = strlen(player1);
    int len2 = strlen(player2);

    // Convert player1 input to lowercase
    for (int i = 0; i < len1; i++)
    {
        player1[i] = tolower(player1[i]);
    }

    // Convert player2 input to lowercase
    for (int i = 0; i < len2; i++)
    {
        player2[i] = tolower(player2[i]);
    }

    // Calculate Player 1 score
    for (int i = 0; i < len1; i++)
    {
        for (int j = 0; j < LEN_ALPHABET; j++)
        {
            if (player1[i] == alphabet[j])
                PLAYER1_SCORE += values[j];
        }
    }
    printf("Player 1 score: %i\n", PLAYER1_SCORE);

    // Calculate Player 2 score
    for (int i = 0; i < len2; i++)
    {
        for (int j = 0; j < LEN_ALPHABET; j++)
        {
            if (player2[i] == alphabet[j])
                PLAYER2_SCORE += values[j];
        }
    }
    printf("Player 2 score: %i\n", PLAYER2_SCORE);
    if (PLAYER1_SCORE > PLAYER2_SCORE)
        printf("Player 1 wins!\n");
    else if (PLAYER1_SCORE < PLAYER2_SCORE)
        printf("Player 2 wins!\n");
    else
        printf("Tie!\n");
}
