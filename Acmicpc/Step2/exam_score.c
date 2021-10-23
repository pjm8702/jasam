#include <stdio.h>

int main(void)
{
    int score;

    scanf("%d", &score);
    if(score >= 90 && score <= 100)
        printf("%c\n", 'A');
    else if(score >= 80 && score <= 89)
        printf("%c\n", 'B');
    else if(score >= 70 && score <= 79)
        printf("%c\n", 'C');
    else if(score >= 60 && score <= 69)
        printf("%c\n", 'D');
    else
        printf("%c\n", 'F');
        
    return 0;
}