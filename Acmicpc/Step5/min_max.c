#include <stdio.h>

int main(void)
{
    int N, i;
    int min = 1000000, max = -1000000, tmp;

    scanf("%d", &N);
    for(i = 0; i < N; i++)
    {
        scanf("%d", &tmp);
        if(tmp > max)
            max = tmp;
        if(tmp < min)
            min = tmp;
    }

    printf("%d %d\n", min, max);

    return 0;
}