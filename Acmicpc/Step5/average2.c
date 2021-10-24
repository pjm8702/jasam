#include <stdio.h>

int main(void)
{
    int C, N, cnt = 0, i, j, sum = 0;
    int score[1000] = {0,};
    double avg;
    
    scanf("%d", &C);
    for(i = 0; i < C; i++)
    {
        scanf("%d", &N);
        for(j = 0; j < N; j++)
        {
            scanf("%d", &score[j]);
            sum += score[j];
        }

        avg = (double)sum / N;
        sum = 0;

        for(j = 0; j < N; j++)
        {
            if((double)score[j] > avg)
            {
                cnt++;
                score[j] = 0;
            }
        }

        printf("%.3lf%%\n", (double)cnt/N*100);   
        cnt = 0;     
    }

    return 0;
}