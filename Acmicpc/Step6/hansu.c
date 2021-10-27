#include <stdio.h>

int hansu(int n)
{
    int i, div = 1000, tmp = n;
    int arr[4] = {0,};

    if(n <= 99)
        return 1;
    
    for(i = 0; i < 4; i++)
    {
        arr[i] = tmp / div;
        tmp = tmp - ((tmp/ div) * div);
        div /= 10;
    }

    if(arr[0] == 0)
    {
        if(arr[1] - arr[2] == arr[2] - arr[3])
            return 1;
    }
    else
    {
        if((arr[0] - arr[1] == arr[1] - arr[2]) && (arr[1] - arr[2] == arr[2] - arr[3]))
            return 1;
    }

    return 0;
}

int main(void)
{
    int N, i, cnt = 0;

    scanf("%d", &N);
    for(i = 1; i <= N; i++)
    {
        if(hansu(i))
            cnt++;
    }
    printf("%d\n", cnt);

    return 0;
}