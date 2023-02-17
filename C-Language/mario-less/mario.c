#include <cs50.h>
#include <stdio.h>



int main(void)
{
//Ask for the integers
    int n = 0 ;

    do

    {
        n = get_int("Type in an positive integer between 1 and 8: ");
    }
    while (!((n <= 8) && (n >= 1)));




    //Main Function
    // Make a line
    for (int line = 0; line < n; line++)
    {
        //Make a space
        for (int space = 0; space < n - line - 1; space++)
        {
                  printf(" ");
        }
        //Make a hash
        for (int hash = 0; hash < line + 1; hash++)
        {

                  printf("#");

                  
        }
        printf("\n");
    }
}

