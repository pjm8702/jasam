#include <stdio.h>
#include <stdlib.h>


int main(void)
{
    int N, M;
    int i = 0, j;
    int **elevator;
    int speed = 0, tmp_speed = 0;
    int tmp_distance = 0;

    scanf("%d %d", &N, &M);
    elevator = (int**)calloc(N + M, sizeof(int*));
    for(i = 0; i < N + M; i++)
    {
        elevator[i] = (int*)calloc(2, sizeof(int));
        scanf("%d %d", &elevator[i][0], &elevator[i][1]);
    }

    i = 0;
    j = N;
    while(1)
    {
        tmp_distance = elevator[j][0] - elevator[i][0];
        tmp_speed = elevator[j][1] - elevator[i][1];
        if(tmp_speed > 0 && tmp_speed > speed)
        {
            speed = tmp_speed;
        }

        if(tmp_distance > 0)
        {
            elevator[j][0] = tmp_distance;
            i++;
        }
        else if(tmp_distance < 0)
        {
            elevator[i][0] = tmp_distance * -1;
            j++;
        }
        else
        {
            i++;
            j++;
        }

        if(i == N && j == N + M)
            break;
    }

    printf("%d\n", speed);

    for(i = 0; i < N + M; i++)
        free(elevator[i]);
    free(elevator);
  
  return 0;
}
