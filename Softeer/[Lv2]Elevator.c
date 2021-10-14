/*
[Lv2]Elevator.c 
0m 부터 100m까지 일정 구간들의 엘리베이터 속도를 검사하는 업무를 맡게 되었다. 빌딩에서 운영되는 엘리베이터 구간은 N개의 구간으로 나뉘며 해당 구간의 제한 속도이 주어진다. 
구간의 총 합은 100m 이며 각 구간별 구간의 길이와 제한 속도 모두 양의 정수로 주어진다. 예를 들어보자. 구간이 3이라고 할 때 

▶ 첫 번째 구간의 길이는 50m 이고 제한 속도는 50m/s
▶ 두 번째 구간의 길이는 40m 이고 제한 속도는 40m/s 
▶ 세 번째 구간의 길이는 10m 이고 제한 속도는 30m/s 

임의의 구간의 길이와 속도를 정하여 시범운행 할 때, 가장 제한 속도가 크게 벗어난 값을 스스로 구해야 한다. M개의 구간을 검사한다고 할 때 예를 들면,

▶ 첫 번째 구간의 운행 길이는 60m 이고 속도는 76m/s
▶ 두 번째 구간의 운행 길이는 18m 이고 속도는 28m/s
▶ 세 번째 구간의 운행 길이는 22m 이고 속도는 50m/s 이라고 했을 때 제한 속도를 벗어나 가장 차이가 큰 속도를 구해 보자.

첫번째 구간 50m 까지에서 제한 속도와 실제 운행 속도를 비교했을 때, 제한 속도를 26m/s 초과했다. 
이후 두번째 구간과 실 운행한 첫번째 구간이 10m 정도 겹치는데, 이때 제한 속도를 36m/s 초과하게 된다. 
그 이후 구간들에서는 차이가 그보다 크지 않으므로 가장 큰 속도 차이는 36m/s임을 알 수 있다. 
주어진 구간의 제한속도와 광우가 테스트한 구간의 속도를 기준으로 가장 크게 제한 속도를 넘어간 값이 얼마인지 구해보자.

[입력형식] 
첫 줄에 N과 M이 주어진다. 그 다움 줄부터 N개의 줄은 각 구간의 길이 및 해당 구간에서의 제한 속도가 주어지며, 다음 M개의 줄은 광우가 테스트하는 구간의 길이와 속도가 주어진다.

[출력형식] 
제한 속도를 가장 크게 벗어난 값을 출력 한다. 단 제한 속도를 벗어나지 않은 경우는 0을 출력 한다.

[입력예제1] 
3 3 
50 50 
40 40 
10 30 
60 76 
18 28 
22 50

[출력예제1] 
36

[입력예제2] 
3 3
50 90
10 90
40 50
50 40
10 100
40 40

[출력예제2] 
10
*/

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
