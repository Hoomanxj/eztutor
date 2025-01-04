// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 252525;
// keep track of word count in the dictionary
unsigned int word_counter = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    unsigned int index = hash(word);
    for (node *tmp = table[index]; tmp != NULL; tmp = tmp->next)
    {
        if (strcasecmp(tmp->word, word) == 0)
        {
            return true;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    const int two_digit = 9;
    int l1 = toupper(word[0]) - 'A';
    int l2 = 0;
    int l3 = 0;
    if (strlen(word) >= 2) // Check if the word has 2 or more letters
    {
        l2 = toupper(word[1]) - 'A';
    }

    if (strlen(word) >= 3) // Check if the word has 3 or more letters
    {
        l3 = toupper(word[2]) - 'A';
    }

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
    return (l3 + l2 + l1) % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    FILE *source = fopen(dictionary, "r");
    if (source == NULL)
    {
        printf("Could not open dictionary file.\n");
        return false;
    }
    char value[LENGTH + 1];

    while (fscanf(source, "%s", value) != EOF)
    {
        node *new_word = malloc(sizeof(node));
        if (new_word == NULL)
        {
            return false; // Handle memory allocation failure
        }
        unsigned int index = hash(value);

        strcpy(new_word->word, value);
        new_word->next = table[index];
        table[index] = new_word;

        // update the word count in dictionary
        word_counter++;
    }
    fclose(source);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return word_counter;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        node *counter = table[i];
        while (counter != NULL)
        {
            node *tmp = counter;
            counter = counter->next;
            free(tmp);
        }
    }
    return true;
}
