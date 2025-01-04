#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

// make command-line take 1 argument
int main(int argc, string argv[])
{
    if (!(argc == 2)) // for anything but 1 argument produce an error
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    // check if the number of characters matches the whole alphabet
    int ALPHABET_C = 26;
    string key = argv[1];
    int key_len = strlen(key);

    if (!(key_len == ALPHABET_C))
    {
        printf("key must contain 26 characters\n");
        return 1;
    }
    else
    {
        for (int i = 0; i < key_len; i++)
        { // check if the characters are from alphabet
            if (!(isalpha(key[i])))
            {
                printf("key must contain alphabet characters\n");
                return 1;
            }
            // check if there are duplicate characters
            for (int j = 0; j < key_len; j++)
                if ((tolower(key[i]) == tolower(key[j])) && (i != j))
                {
                    printf("key cannot contain duplicate characters\n");
                    return 1;
                }
        }
    }

    // get the plaintext from the user
    string plaintext = get_string("Plaintext: ");
    int plaintext_len = strlen(plaintext);
    char ciphertext[plaintext_len + 1];

    // use the key to decrypt the plaintext
    for (int i = 0; i < plaintext_len; i++)
    {
        if (islower(plaintext[i]))
        {
            ciphertext[i] = tolower(key[plaintext[i] - 'a']);
        }
        else if (isupper(plaintext[i]))
        {
            ciphertext[i] = toupper(key[plaintext[i] - 'A']);
        }
        else
        {
            ciphertext[i] = plaintext[i];
        }
    }
    ciphertext[plaintext_len] = '\0';
    printf("ciphertext: %s\n", ciphertext);
    return 0;
}
