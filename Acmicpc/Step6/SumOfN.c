#include <stdio.h>

long long sum(int *a, int n)
{
    int i;
    long long sum = 0;

    for(i = 0; i < n; i++)
        sum += a[i];
    
    return sum;
}