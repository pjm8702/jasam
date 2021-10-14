/*
[Lv2]GearShift.c 
1단에서 8단으로 연속적으로 변속을 한다면 ascending, 8단에서 1단으로 연속적으로 변속한다면 descending, 둘다 아니라면 mixed 라고 정의했다. 
순서가 주어졌을 때 이것이 ascending인지, descending인지, 아니면 mixed인지 출력하는 프로그램을 작성하시오.

[입력형식] 
첫째 줄에 8개 숫자가 주어진다. 1부터 8까지 숫자가 한번씩 등장한다.

[출력형식] 
첫째 줄에 ascending, descending, mixed 중 하나를 출력한다.

[입력예제] 
1 2 3 4 5 6 7 8

[출력예제] 
ascending
*/

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
