#include <stdio.h>
#include <string.h>

int main(void)
{
    int T, R, i, j, k;
    char S[20] = {'\0',};

    scanf("%d", &T);
    for(i = 0; i < T; i++)
    {
        scanf("%d %s", &R, S);
        for(j = 0; j < strlen(S); j++)
        {
            for(k = 0; k < R; k++)
                printf("%c", S[j]);
        }
        printf("\n");
    }

    return 0;
}