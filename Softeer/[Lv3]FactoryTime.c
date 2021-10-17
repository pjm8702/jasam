/*
동일한 자동차를 생산하는 2개의 조립 라인 A와 B가 있다. 두 조립라인에는 각각 N개의 작업장이 있다. 각각의 작업장을 Ai (1 ≤ i ≤ N)와 Bi (1 ≤ i ≤ N)로 표시하자.
Ai 작업장과 Bi 작업장은 동일한 작업을 수행하지만 작업시간은 다를 수 있다. 
A 조립 라인의 경우 A1 작업장에서 최초 조립이 시작되고, Ai 작업장에서 작업이 종료되면 바로 Ai+1 작업장에서 작업을 시작할 수 있다.
B 조립 라인도 동일한 방식으로 조립을 진행한다. 
Ai 작업장에서 Bi+1작업장으로 혹은 Bi 작업장에서 Ai+1작업장으로 반조립 제품의 이동이 가능(이동시간이 추가됨)할 때 자동차 1대의 가장 빠른 조립 시간을 구하여라.

[입력형식]
첫 번째 줄에 작업장의 수 N이 주어진다. i+1 (1 ≤ i ≤ N-1) 번째 줄에는 Ai 작업장의 작업시간, Bi 작업장의 작업시간, Ai 작업장에서 Bi+1 작업장까지 이동시간, Bi 작업장에서 Ai+1 작업장까지 이동시간이 차례로 주어진다. 
마지막 N+1번째 줄에는 AN 작업장과 BN 작업장의 작업시간이 주어진다.

입력은 다음 조건을 만족한다.

   1 ≤ N ≤ 103 인 정수
   각 작업시간과 이동시간은 105을 넘지 않는 양의 정수

[출력형식]
첫 번째 줄에 가장 빠른 조립시간을 출력하라.

[입력예제]
2
1 3 1 2
10 2

[출력예제]
4
*/

#include <stdio.h>
#include <stdlib.h>

typedef struct{
    int work_time;
    int move_time;
} Factory;

int main(void)
{
    int N, i;
    Factory *factory[2];
    int *time[2];

    scanf("%d", &N);
    for(i = 0; i < 2; i++)
    {
        factory[i] = (Factory*)calloc(N, sizeof(Factory));
        time[i] = (int*)calloc(N, sizeof(int));
    }

    for(i = 0; i < N; i++)
    {
        if(i == N-1)
        {
            scanf("%d %d", &(factory[0][i].work_time), &(factory[1][i].work_time));
        }
        else
        {
            scanf("%d %d %d %d", &(factory[0][i].work_time), &(factory[1][i].work_time), &(factory[0][i].move_time), &(factory[1][i].move_time));
        }
    }

    time[0][0] = factory[0][0].work_time;
    time[1][0] = factory[1][0].work_time;    
    for(i = 1 ; i < N; i++)
    {
        if(time[0][i-1] < time[1][i-1] + factory[1][i-1].move_time)
        {
            time[0][i] = time[0][i-1] + factory[0][i].work_time;
        }
        else
        {
            time[0][i] = time[1][i-1] + factory[1][i-1].move_time + factory[0][i].work_time;
        }

        if(time[1][i-1] < time[0][i-1] + factory[0][i-1].move_time)
        {
            time[1][i] = time[1][i-1] + factory[1][i].work_time;
        }
        else
        {
            time[1][i] = time[0][i-1] + factory[0][i-1].move_time + factory[1][i].work_time;
        }
    }

    if(time[0][N - 1] > time[1][N - 1])
    {
        printf("%d\n", time[1][N-1]);
    }
    else
    {
        printf("%d\n", time[0][N-1]);
    }

    free(factory[0]);
    free(factory[1]);
    free(time[0]);
    free(time[1]);
  return 0;
}
