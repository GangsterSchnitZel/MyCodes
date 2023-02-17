// Implements a dictionary's functionality
#include <strings.h>
#include <stdio.h>
#include <ctype.h>
#include <stdbool.h>
#include "dictionary.h"
#include <stdlib.h>
#include <string.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

//Variables
unsigned int counter = 0;
unsigned int hash_value;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    hash_value = hash(word);

    node *cursor = table[hash_value];
    //Loop through the end
    while(cursor != 0)
    {
        if(strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        //else move to next
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    //Take String Return Index
    unsigned long hash = 0;
    int i=0;
    while (i < strlen(word))
    {
        i++;
        hash += tolower(word[i]);
    }
    return (hash % N);
    // I tried to make the tolower function faster with an ASCII lookup table from STACKOVERFLOW. But I
    // couldn't get it implemented.

}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    //Open the file
    FILE *dict = fopen(dictionary,"r");

    //Check if there is a readable dictfile
    if (dict == NULL)
    {
        printf("Can't open file %s\n", dictionary);
        return false;
    }
    char word[LENGTH+1];

    while(fscanf(dict, "%s", word) != EOF)
    {
        //Malloc memory for node
        node *n = malloc(sizeof(node));
        //Return if not succesfull
        if(n == NULL)
        {
            return false;
        }
        // Copy string in node
        strcpy(n->word, word);
        hash_value = hash(word);
        n->next = table[hash_value];
        table[hash_value] = n;
        counter+=1;
    }
    //Close file
    fclose(dict);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    if(counter > 0)
    {
        return counter;
    }
    return 0;
}





// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for(int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while(cursor)
        {
            node *tmp = cursor;
            cursor = cursor-> next;
            free(tmp);
        }
        if (i == N - 1  && cursor == NULL)
        {
            return true;
        }
    }
    return false;
}
