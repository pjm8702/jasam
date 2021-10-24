#include <stdio.h>

int main(void)
{
    int N, a, b, c, newN;
    int cnt = 0;

    scanf("%d", &N);
    newN = N;
    while(1)
    {
        cnt++;
        a = newN / 10;
        b = newN % 10;
        c = (a + b) % 10;
        if((b * 10) + c == N)
            break;
        else
            newN = (b * 10) + c;
    }

    printf("%d\n", cnt);

    return 0;
}