#include <stdio.h>

#define LEN 9

int main(void)
{
    int arr[LEN] = {0,};
    int i, max = 0, idx;

    for(i = 0; i < LEN; i++)
    {
        scanf("%d", &arr[i]);
        if(arr[i] > max)
        {
            max = arr[i];
            idx = i + 1;
        }
    }

    printf("%d\n%d\n", max, idx);

    return 0;
}