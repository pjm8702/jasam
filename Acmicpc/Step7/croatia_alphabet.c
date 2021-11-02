#include <stdio.h>
#include <string.h>

int main(void)
{
    char str[101] = {'\0'};
    int i, j, cnt = 0;

    scanf("%s", str);
    for(i = 0; i < strlen(str); i++)
    {
        if((str[i] == 'c' && (str[i+1] == '=' || str[i+1] == '-'))
         || (str[i] == 'd' && str[i+1] == '-') 
         || (str[i] == 'l' && str[i+1] == 'j')
         || (str[i] == 'n' && str[i+1] == 'j')
         || (str[i] == 's' && str[i+1] == '=')
         || (str[i] == 'z' && str[i+1] == '='))
        {
            cnt++;
            i++;
        }
        else if(str[i] == 'd' && str[i+1] == 'z' && str[i+2] == '=')
        {
            cnt++;
            i += 2;
        }
        else
            cnt++;
    }

    printf("%d\n", cnt);

    return 0;
}