#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int N, i, j = 0, cnt = 0, point = 0;
    char ox[81] = {'\0'};
    char ch;

    scanf("%d", &N);
    for(i = 0; i < N; i++)
    {
        scanf("%s", ox);
        for(j = 0; ox[j] != '\0'; j++)
        {
            if(ox[j] == 'O')
            {
                point = point + (++cnt);
                ox[j] = '\0';
            }
            else
                cnt = 0;
        }

        printf("%d\n", point);
        point = cnt = 0;
    }

    return 0;
}