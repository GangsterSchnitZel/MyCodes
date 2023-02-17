#include "helpers.h"
#include <math.h>

#define RED_COLOR 0
#define GREEN_COLOR 1
#define BLUE_COLOR 2

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{

    double average;
    //loop through height
    for (int i = 0; i < height; i++)
    {
        //loop through width
        for (int j = 0; j < width; j++)
        {
            average = (image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0;
            image[i][j].rgbtRed = image[i][j].rgbtGreen = image[i][j].rgbtBlue = round(average);
        }
    }

    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{

    float red, blue, green;
    //loop through height
    for (int i = 0; i < height; i++)
    {
        //loop through width
        for (int j = 0; j < width; j++)
        {
            red = image[i][j].rgbtRed;
            green = image[i][j].rgbtGreen;
            blue = image[i][j].rgbtBlue;

            int sepiaRed = round(0.393 * red + 0.769 * green + 0.189 * blue);

            int sepiaGreen = round(0.349 * red + 0.686 * green + 0.168 * blue);

            int sepiaBlue = round(0.272 * red + 0.534 * green + 0.131 * blue);

            image[i][j].rgbtRed = fmin(255, sepiaRed);
            image[i][j].rgbtGreen = fmin(255, sepiaGreen);
            image[i][j].rgbtBlue = fmin(255, sepiaBlue);

        }
    }


    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{

    RGBTRIPLE temporary;

    //loop through height
    for (int i = 0; i < height; i++)
    {
        //loop through width
        for (int j = 0; j < width / 2; j++)
        {
            temporary = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = temporary;

        }


    }

    return;
}

int Blur(int i, int j, int height, int width, RGBTRIPLE image[height][width], int color_position)
{
    float count = 0;
    int sum = 0;
    for (int row = i - 1; row <= (i + 1); row++)
    {
        for (int column = j - 1; column <= (j + 1); column++)
        {
            if (row < 0 || row >= height || column < 0 || column >= width)
            {
                continue;
            }
            if (color_position == RED_COLOR)
            {
                sum += image[row][column].rgbtRed;
            }
            else if (color_position == GREEN_COLOR)
            {
                sum += image[row][column].rgbtGreen;
            }
            else
            {
                sum += image[row][column].rgbtBlue;
            }
            count++;
        }

    }
    return round(sum / count);

}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{

    RGBTRIPLE clone[height][width];

    //loop through height
    for (int i = 0; i < height; i++)
    {
        //loop through width
        for (int j = 0; j < width; j++)
        {
            clone[i][j] = image[i][j];
        }

    }

    //loop through height
    for (int i = 0; i < height; i++)
    {
        //loop through width
        for (int j = 0; j < width; j++)
        {

            image[i][j].rgbtRed = Blur(i, j, height, width, clone, RED_COLOR);
            image[i][j].rgbtGreen = Blur(i, j, height, width, clone, GREEN_COLOR);
            image[i][j].rgbtBlue = Blur(i, j, height, width, clone, BLUE_COLOR);

        }

    }


    return;
}
