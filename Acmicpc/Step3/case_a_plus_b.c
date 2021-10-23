#include <stdio.h>

int main(void)
{
    int N, a, b, i;

    scanf("%d", &N);
    for(i = 0; i < N; i++)
    {
        scanf("%d %d", &a, &b);
        printf("Case #%d: %d\n", i + 1, a + b);
    }
    return 0;
}