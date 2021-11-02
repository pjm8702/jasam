#include <stdio.h>
#include <string.h>

int main(void)
{
    char str[100] = {'\0',};
    int find['z' - 'a' + 1] = {-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1};
    int i;

    scanf("%s", str);
    for(i = 0; i < strlen(str); i++)
    {
        if(find[str[i] - 'a'] == -1)
            find[str[i] - 'a'] = i;
    }

    for(i = 0; i < 'z' - 'a' + 1; i++)
        printf("%d ", find[i]);

    return 0;
}