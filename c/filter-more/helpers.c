#include "helpers.h"
#include <math.h>
#include <stdlib.h>
#include <string.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int avg =
                round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
            image[i][j].rgbtBlue = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtRed = avg;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            // swap left with right
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE blurred[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int r_avg = 0, g_avg = 0, b_avg = 0;
            int counter = 0;

            for (int x = i - 1; x <= i + 1; x++)
            {
                for (int y = j - 1; y <= j + 1; y++)
                {
                    // Check that pixel is within image boundaries
                    if (x >= 0 && x < height && y >= 0 && y < width)
                    {
                        r_avg += image[x][y].rgbtRed;
                        g_avg += image[x][y].rgbtGreen;
                        b_avg += image[x][y].rgbtBlue;
                        counter++;
                    }
                }
            }

            // Assign the blurred values, making sure division is accurate
            blurred[i][j].rgbtRed = round(r_avg / (float) counter);
            blurred[i][j].rgbtGreen = round(g_avg / (float) counter);
            blurred[i][j].rgbtBlue = round(b_avg / (float) counter);
        }
    }

    // Copy blurred image back into the original image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = blurred[i][j];
        }
    }

    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    int BLACK = 255;
    // define grid coefficients of gx and gy as a matrix
    int gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    // use enum() to enable interpretation of letters as numbers
    enum { x, y };
    enum { r, g, b };

    // temporary canvas to hold pixel values
    RGBTRIPLE blurred[height][width];

    // loop through every single pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sobel[2][3] = {{0, 0, 0}, {0, 0, 0}}; // Reset Sobel values for each pixel

            // Loop through the 3x3 grid around the current pixel
            for (int m = -1; m <= 1; m++)
            {
                for (int n = -1; n <= 1; n++)
                {
                    // Calculate the neighboring pixel position
                    int neighbor_i = i + m;
                    int neighbor_j = j + n;

                    // Check for boundaries
                    if (neighbor_i >= 0 && neighbor_i < height && neighbor_j >= 0 &&
                        neighbor_j < width)
                    {
                        // Map m and n to 3x3 kernel indices
                        int kernel_row = m + 1;
                        int kernel_col = n + 1;

                        // Apply Sobel Gx filter for each color channel
                        sobel[x][r] +=
                            image[neighbor_i][neighbor_j].rgbtRed * gx[kernel_row][kernel_col];
                        sobel[x][g] +=
                            image[neighbor_i][neighbor_j].rgbtGreen * gx[kernel_row][kernel_col];
                        sobel[x][b] +=
                            image[neighbor_i][neighbor_j].rgbtBlue * gx[kernel_row][kernel_col];

                        // Apply Sobel Gy filter for each color channel
                        sobel[y][r] +=
                            image[neighbor_i][neighbor_j].rgbtRed * gy[kernel_row][kernel_col];
                        sobel[y][g] +=
                            image[neighbor_i][neighbor_j].rgbtGreen * gy[kernel_row][kernel_col];
                        sobel[y][b] +=
                            image[neighbor_i][neighbor_j].rgbtBlue * gy[kernel_row][kernel_col];
                    }
                }
            }

            // Calculate the final Sobel filter values and apply the edge detection
            int sobel_filter[3];
            sobel_filter[r] =
                round(sqrt((sobel[x][r] * sobel[x][r]) + (sobel[y][r] * sobel[y][r])));
            sobel_filter[g] =
                round(sqrt((sobel[x][g] * sobel[x][g]) + (sobel[y][g] * sobel[y][g])));
            sobel_filter[b] =
                round(sqrt((sobel[x][b] * sobel[x][b]) + (sobel[y][b] * sobel[y][b])));

            // Ensure the values don't exceed the maximum allowed (255)
            for (int k = 0; k < 3; k++)
            {
                if (sobel_filter[k] > BLACK)
                    sobel_filter[k] = BLACK;
            }

            // Store color values for each blurred pixel
            blurred[i][j].rgbtRed = sobel_filter[r];
            blurred[i][j].rgbtGreen = sobel_filter[g];
            blurred[i][j].rgbtBlue = sobel_filter[b];
        }
    }

    // Replace each original pixel with blurred ones
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = blurred[i][j];
        }
    }

    return;
}
