#include <stdio.h>

int main(void)
{
    int a, b;

    scanf("%d %d", &a, &b);
    if(a > b)
        printf("%c\n", '>');
    else if(a < b)
        printf("%c\n", '<');
    else
        printf("%s\n", "==");

    return 0;
}