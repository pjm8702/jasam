#include <stdio.h>
#include <string.h>

int main(void)
{
    int N, i, j, cnt = 0, chk = 0;
    char str[101] = {'\0'};
    int alphabet[26] = {0,};

    scanf("%d", &N);
    for(i = 0; i < N; i++)
    {
        scanf("%s", str);
        alphabet[str[0] - 'a'] = 1;
        for(j = 1; j < strlen(str); j++)
        {
            if(str[j-1] != str[j])
            {
                if(alphabet[str[j] - 'a'] == 0)
                    alphabet[str[j] - 'a'] = 1;
                else
                    chk = 1;
            }
        }
        if(chk == 0)
            cnt++;
        chk = 0;

        for(j = 0; j < strlen(str); j++)
            str[j] = '\0';
        
        for(j = 0; j < 26; j++)
            alphabet[j] = 0;
    }

    printf("%d\n", cnt);

    return 0;
}