#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int T, a, b, i;
    int *sum;

    scanf("%d", &T);
    sum = (int*)calloc(T, sizeof(int));
    for(i = 0; i < T; i++)
    {
        scanf("%d %d", &a, &b);
        sum[i] = a + b;
    }

    for(i = 0; i < T; i++)
        printf("%d\n", sum[i]);

    free(sum);
    return 0;
}