#include <stdio.h>
#include <string.h>

int main(void)
{
    char str[16] = {'\0',};
    int i, second = 0;

    scanf("%s", str);
    for(i = 0; i < strlen(str); i++)
    {
        if(str[i] >= 'A' && str[i] <= 'C')
            second += 3;
        else if(str[i] >= 'D' && str[i] <= 'F')
            second += 4;
        else if(str[i] >= 'G' && str[i] <= 'I')
            second += 5;
        else if(str[i] >= 'J' && str[i] <= 'L')
            second += 6;
        else if(str[i] >= 'M' && str[i] <= 'O')
            second += 7;
        else if(str[i] >= 'P' && str[i] <= 'S')
            second += 8;
        else if(str[i] >= 'T' && str[i] <= 'V')
            second += 9;
        else if(str[i] >= 'W' && str[i] <= 'Z')
            second += 10;    
    }

    printf("%d\n", second);

    return 0;
}