#include <stdio.h>

int main(void)
{
    char ch;
    int cnt = 0, start = 0;

    while(1)
    {
        if((ch = getchar()) == '\n')
            break;
        
        if(start == 0 && (ch >= 'a' && ch <= 'z') || (ch >= 'A' && ch <= 'Z'))
            start = 1;
        
        if(start == 1 && ch == ' ')
        {
            cnt++;
            start = 0;
        }
    }

    if(start == 1)
        cnt++;

    printf("%d\n", cnt);

    return 0;
}