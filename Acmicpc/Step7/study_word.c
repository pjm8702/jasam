#include <stdio.h>

int main(void)
{
    char ch;
    int cnt[26] = {0,};
    int i, idx, max, flg = 0;
    
    while(1)
    {
        if((ch = getchar()) == '\n')
            break;
        
        if(ch >= 'a' && ch <= 'z')
            cnt[ch - 'a']++;
        else if(ch >= 'A' && ch <= 'Z')
            cnt[ch - 'A']++;
    }

    max = cnt[0];
    idx = 0;
    for(i = 1; i < 26; i++)
    {
        if(cnt[i] > max)
        {
            max = cnt[i];
            idx = i;
            flg = 0;
        }
        else if(cnt[i] == max)
            flg = 1;
    }

    if(flg == 1)
        printf("%c\n", '?');
    else
        printf("%c\n", 'A' + idx);

    return 0;
}