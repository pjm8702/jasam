#include <stdio.h>

int self_number(int n)
{
    int i, j, self_num, div, num;

    if(n == 1)
        return 0;
    else
    {
        for(i = 1; i <= n; i++)
        {
            self_num = num = i;
            div = 10000;
            for(j = 0; j < 5; j++)
            {
                self_num = self_num + (num / div);
                num = num - (num / div) * div;
                div /= 10;
            }

            if(self_num == n)
                return 1;
        }

        return 0;
    }
}

int main(void)
{
    int i, ret;
    for(i = 1; i <= 10000; i++)
    {
        if(self_number(i) == 0)
            printf("%d\n", i);
    }
    return 0;
}