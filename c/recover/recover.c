#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // check if the name of the file is given in the command line
    if (argc != 2)
    {
        printf("You need to specify the forensic file\n");
        return 1;
    }

    // open the file and check if it can be opened
    FILE *f = fopen(argv[1], "r");
    if (f == NULL)
    {
        printf("the file cannot be opened for reading\n");
        return 1;
    }

    // Allocate memory for the buffer and check
    uint8_t *buffer = malloc(512);
    if (buffer == NULL)
    {
        printf("Memory allocation failed.\n");
        return 1;
    }

    // Allocate memory for image filenames
    char *images = malloc(8 * sizeof(char));
    if (images == NULL)
    {
        printf("Memory allocation for filenames failed.\n");
        return 1;
    }

    int counter = 0;
    FILE *img = NULL;

    while ((fread(buffer, 512, 1, f)) > 0)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // If an image is already open, close it
            if (img != NULL)
            {
                fclose(img);
            }

            // Create a new filename and open a new file
            sprintf(images, "%03i.jpg", counter);
            img = fopen(images, "w");
            if (img == NULL)
            {
                printf("Could not create file.\n");
                return 1;
            }
            counter++;
        }
        // Write the block to the currently open image file (if there is one)
        if (img != NULL)
        {
            fwrite(buffer, 512, 1, img);
        }
    }

    // Close any remaining open files
    if (img != NULL)
    {
        fclose(img);
    }
    fclose(f);
    free(buffer);
    free(images);

    return 0;
}
