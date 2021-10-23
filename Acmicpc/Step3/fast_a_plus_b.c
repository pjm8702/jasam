#include <stdio.h>

int main(void)
{
    int T, a, b, i;

    scanf("%d", &T);
    for(i = 0; i < T; i++)
    {
        scanf("%d %d", &a, &b);
        printf("%d\n", a + b);
    }

    return 0;
}