#include <stdio.h>

int main(void)
{
    int N, X, i, n;

    scanf("%d %d", &N, &X);
    for(i = 0; i < N; i++)
    {
        scanf("%d", &n);
        if(n < X)
            printf("%d ", n);
    }

    return 0;
}