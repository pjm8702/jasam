#include <stdio.h>


int main(void)
{
    int i, up = 0, down = 0;
    int gear[8] = {0,};

    for(i = 0; i < 8; i++)
    {
        scanf("%d", &gear[i]);
    }

    for(i = 0; i < 8; i++)
    {
        if(gear[i] == i + 1)
        {
            up++;
        }
        else if(gear[i] == 8 - i)
        {
            down++;
        }
    }

    if(up < 8 && down < 8)
    {
        printf("%s\n", "mixed");
    }
    else if(up == 8)
    {
        printf("%s\n", "ascending");
    }
    else
    {
        printf("%s\n", "descending");
    }
    
    return 0;
}
