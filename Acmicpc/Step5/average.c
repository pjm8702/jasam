#include <stdio.h>

int main(void)
{
    int N, i, max = 0;
    int grade[1000] = {0,};
    double sum = 0;

    scanf("%d", &N);
    for(i = 0; i < N; i++)
    {
        scanf("%d", &grade[i]);
        if(grade[i] > max)
            max = grade[i];
    }

    for(i = 0; i < N; i++)
        sum += ((double)grade[i] / max) * 100;

    printf("%.9lf\n", sum / N);
    
    return 0;
}