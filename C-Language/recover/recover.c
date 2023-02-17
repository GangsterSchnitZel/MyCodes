#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#define BLOCK_SIZE 512






int main(int argc, char *argv[])
{



//define var and open the memory card file card.raw
    typedef uint8_t BYTE;
    BYTE buffer[BLOCK_SIZE];
    int read = 0;
    int counter = 0;
    char filename[8];

    FILE *f = fopen(argv[1], "r");
    FILE *img = NULL;
// Ensure proper usage
    if (argc != 2)
    {
        printf("Usage: ./recover FILE.raw\n");
        return 1;
    }
    if (f == NULL)
    {
        printf("FILE NOT FOUND \n");
        return 1;
    }

//Read 512 bytes into a buffer
    while (true)
    {
        read = fread(buffer, sizeof(BYTE), 512, f);

//look through that file and look for jpeg beginnings like 0xff 0xd8 0xff
// Fourth last bite is one of 0xe0, 0xe1, 0xe2, 0xe3, 0xe4, 0xe5, 0xe6, 0xe7, 0xe8, 0xe9, 0xea, 0xeb, 0xec, 0xed, 0xee, or 0xef
        if ((buffer[0] == 0xff) && (buffer[1] == 0xd8) && (buffer[2] == 0xff) && ((buffer[3] & 0xf0) == 0xe0))
        {

            if (counter == 0)
            {
                //open new jpeg file and name it in three decimal digits. Starting at 000
                sprintf(filename, "%03i.jpg", counter);
                img = fopen(filename, "w");
                //Jpegs are stored back to back, write 512 bytes in file until a new jpeg is found
                fwrite(buffer, sizeof(BYTE), read, img);
                counter++;
            }
            // if jpeg ends
            else
            {
                fclose(img);
                sprintf(filename, "%03i.jpg", counter);
                img = fopen(filename, "w");
                fwrite(buffer, sizeof(BYTE), read, img);
                counter++;
            }




        }
        else if (counter != 0)
        {
            fwrite(buffer, sizeof(BYTE), read, img);

            if (read == 0)
            {
                fclose(img);
                fclose(f);
                return 0;
            }
        }
    }
    fclose(img);
    fclose(f);
}