#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    // Prompt the user for some text
    string text = get_string("Enter your text please:\n");
    int text_len = strlen(text);

    // Count the number of letters, words, and sentences in the text
    char punc[] = {'.', '!', '?'};
    int PUNC_LEN = 3;
    int letter_c = 0;
    int word_c = 1;
    int sentence_c = 0;
    for (int i = 0; i < text_len; i++)
    {
        if (isalpha(text[i]))
            letter_c++;
        else if (text[i] == ' ')
            word_c++;
        else
            for (int j = 0; j < PUNC_LEN; j++)
            {
                if (text[i] == punc[j])
                {
                    sentence_c++;
                    break;
                }
            }
    }
    printf("letters: %i\nwords: %i\nsentences: %i\n", letter_c, word_c, sentence_c);

    // Compute the Coleman-Liau index
    float L = (float) letter_c / word_c * 100;
    float S = (float) sentence_c / word_c * 100;
    int index = round(0.0588 * L - 0.296 * S - 15.8);

    // Print the grade level
    if (index < 1)
        printf("Before Grade 1\n");
    else if (index > 16)
        printf("Grade 16+\n");
    else
        printf("Grade %i\n", index);
}
