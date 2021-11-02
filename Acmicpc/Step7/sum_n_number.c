#include <stdio.h>

int main(void)
{
    int N, i, sum = 0;
    char ch[100];

    scanf("%d", &N);
    scanf("%s", ch);
    for(i = 0; i < N; i++)
        sum = sum + (ch[i] - '0');

    printf("%d\n", sum);
    
    return 0;
}