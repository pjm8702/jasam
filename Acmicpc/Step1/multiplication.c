#include <stdio.h>

int main(void)
{
    int a, b;
    int num1, num2, num3;

    scanf("%d", &a);
    scanf("%d", &b);

    num1 = b % 10;
    num2 = ((b - num1) % 100) / 10;
    num3 = (b - num1) / 100;

    printf("%d\n", a * num1);
    printf("%d\n", a * num2);
    printf("%d\n", a * num3);
    printf("%d\n", a * b);

    return 0;
}