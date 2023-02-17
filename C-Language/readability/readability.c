#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_letters(string text);

int count_words(string text);

int count_sentences(string text);




int main(void)
{

    //Get Text from the User
    string text = get_string("Text: ");
    //Save Integers and call the function
    int letters = count_letters(text);

    int words = count_words(text);

    int sentences = count_sentences(text);

    //Calculate with the formula
    float L;
    L = ((float)letters / (float)words) * 100;
    float S;
    S = ((float)sentences / (float)words) * 100;

    float liam = ((float)L * 0.0588) - ((float)S * 0.296) - 15.8;
    int output = (round((float)liam));

    //Output
    if (output < 1)
    {
        printf("Before Grade 1");
    }
    else if ((output > 1) && (output < 16))
    {
        printf("Grade %i", output);
    }
    else if (output >= 16)
    {
        printf("Grade 16+");
    }


    printf("\n");
}

//Function that count letters

int count_letters(string text)
{

    int letters = 0;

    int length = strlen(text);


    for (int i = 0; i < length; i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
    }
    return letters;

}
int count_words(string text)
{

    int words = 0;

    int length = strlen(text);

    char seperators[] = " .,;:?!\n\t";



    for (int i = 0; i < length; i++)
    {
        while (i < length)
        {
            if (strchr(seperators, text[i]) != NULL)
            {
                break;
            }
            i++;
        }
        words++;

        while (i < length)
        {
            if (strchr(seperators, text[i]) == NULL)
            {
                break;
            }
            i++;
        }

    }
    return words;


}

int count_sentences(string text)
{

    int sentences = 0;

    int length = strlen(text);

    char seperators[] = ".?!";



    for (int i = 0; i < length; i++)
    {

        if (strchr(seperators, text[i]) != NULL)
        {
            sentences++;
        }
    }
    return sentences;

}