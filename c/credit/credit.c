#include <cs50.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

// Function prototypes
bool validity(long n);
int luhn_checksum(long number);
void identify_card_type(long number);

int main(void)
{
    // Prompt user for input
    long input = get_long("Number: ");

    // Check card length validity
    if (!validity(input))
    {
        printf("INVALID\n");
        return 0;
    }

    // Check if card passes Luhn's checksum
    if (luhn_checksum(input) != 0)
    {
        printf("INVALID\n");
        return 0;
    }

    // Identify card type based on starting digits and length
    identify_card_type(input);

    return 0;
}

// Check if card length is 13, 15, or 16 digits
bool validity(long number)
{
    int length = 0;
    long temp = number;

    // Count the digits in the number
    while (temp > 0)
    {
        length++;
        temp /= 10;
    }

    // Immediately return false if length is not 13, 15, or 16
    if (length != 13 && length != 15 && length != 16)
    {
        return false;
    }

    return true;
}

// Calculate Luhn checksum for card validity
int luhn_checksum(long number)
{
    int sum = 0;
    bool is_second_digit = false;

    // Loop through digits from the last one
    while (number > 0)
    {
        int digit = number % 10;

        if (is_second_digit)
        {
            digit *= 2;
            if (digit > 9)
            {
                digit -= 9;
            }
        }

        sum += digit;
        is_second_digit = !is_second_digit;
        number /= 10;
    }

    return sum % 10;
}

// Identify and print the card type based on starting digits
void identify_card_type(long number)
{
    int length = 0;
    long temp = number;

    // Calculate length of the number
    while (temp > 0)
    {
        temp /= 10;
        length++;
    }

    // Extract first two digits for card type identification
    long start = number;
    while (start >= 100)
    {
        start /= 10;
    }

    // Check for card type based on length and start digits
    if (length == 15 && (start == 34 || start == 37))
    {
        printf("AMEX\n");
    }
    else if (length == 16 && (start >= 51 && start <= 55))
    {
        printf("MASTERCARD\n");
    }
    else if ((length == 13 || length == 16) && (start / 10 == 4))
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }
}
