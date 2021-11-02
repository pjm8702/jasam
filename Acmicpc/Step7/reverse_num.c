#include <stdio.h>

int main(void)
{
    char num1[4] = {'\0',}, num2[4] = {'\0',};
    int n1 = 0, n2 = 0, i;
    int mul = 100;

    scanf("%s %s", num1, num2);
    for(i = 2; i >= 0; i--)
    {
        n1 = n1 + ((num1[i] - '0') * mul);
        n2 = n2 + ((num2[i] - '0') * mul);
        mul /= 10;
    }

    if(n1 > n2)
        printf("%d\n", n1);
    else
        printf("%d\n", n2);

    return 0;
}