#include <stdio.h>

int main(void)
{
    int num;
    int cnt[10] = {0,};
    int i, mul = 1, div;

    for(i = 0; i < 3; i++)
    {
        scanf("%d", &num);
        mul *= num;
    }

    while(mul != 0)
    {
        div = mul % 10;
        cnt[div]++;
        mul = (mul - div) / 10;

    }

    for(i = 0; i < 10; i++)
        printf("%d\n", cnt[i]);

    return 0;
}