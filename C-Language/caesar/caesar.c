#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>



//Main Function with Command-Line Arguments
int main(int argc, string argv[])
{
//Errormessage if argc is not 2
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
//Errormessage if its not a digit
    int length = strlen(argv[1]);

    for (int i = 0; i < length; i++)
    {
        if (isdigit(argv[1][i]) == 0)
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }

    }
//Convert string to int
    int key = atoi(argv[1]);
    //Enter Plaintext
    string plaintext = get_string("plaintext: ");


    printf("ciphertext: ");

    for (int i = 0; i < strlen(plaintext); i++)
    {



        //Uppercase
        if (isupper(plaintext[i]))

        {

            printf("%c", (plaintext[i] - 65 + key) % 26 + 65);

        }


        //Lowercase
        else if (islower(plaintext[i]))
        {

            printf("%c", (plaintext[i] - 97 + key) % 26 + 97);

        }
        else
        {

            printf("%c", plaintext[i]);

        }
    }


    printf("\n");
}









