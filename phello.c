#include <stdio.h>
#include <pthread.h>

#define NUMT 123

pthread_t threadIDs[NUMT]; /* threadIDs */

void *tfunc(void *p)
{
    // thread work function
}

int main(void)
{
    int i;
    for (i = 0; i < NUMT; i++)
    {
        pthread_create(&threadIDs[i], NULL, tfunc, ???);
    }
    for (i = 0; i < NUMT; i++)
    {
        pthread_join(threadIDs[i], NULL);
    }
}