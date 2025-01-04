#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n = 0;
    while ((n < 1) || (n > 8))
    {
        n = get_int("Height: ");
    }
    int m = n - 1;
    // loop for height
    for (int j = 0; j < n; j++)
    {
        // loop for rows
        for (int i = 0; i < m; i++)
        {
            printf(" ");
        }

        for (int i = 0; i < (n - m); i++)
        {
            printf("#");
        }

        printf("  ");

        for (int i = 0; i < (n - m); i++)
        {
            printf("#");
        }
        printf("\n");
        m--;
    }
}
