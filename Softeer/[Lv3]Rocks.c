/*
남북으로 흐르는 개울에 동서로 징검다리가 놓여져 있다.
이 징검다리의 돌은 들쑥날쑥하여 높이가 모두 다르다.
철수는 개울의 서쪽에서 동쪽으로 높이가 점점 높은 돌을 밟으면서 개울을 지나가려고 한다.
돌의 높이가 서쪽의 돌부터 동쪽방향으로 주어졌을 때 철수가 밟을 수 있는 돌의 최대 개수는?

[입력형식]
첫 번째 줄에 돌의 개수 N이 주어진다.
두 번째 줄에 돌의 높이 Ai (1 ≤ i ≤ N)가 서쪽부터 동쪽으로 차례로 주어진다.

입력은 다음 조건을 만족한다.
    1 ≤ N ≤ 3×103 인 정수
    1 ≤ A ≤ 108 인 정수

[출력형식]
첫 번째 줄에 철수가 밟을 수 있는 돌의 최대 개수를 출력하라.

[입력예제]
5
3 2 1 4 5

[출력예제]
3
*/

#include <stdio.h>
#include <stdlib.h>


int main(void)
{
    int N, i, j, max;
    int bridge[3000] = {0,};
    int rocks[3000] = {1,};

    scanf("%d", &N);
    for(i = 0; i < N; i++)
    {
        scanf("%d", &bridge[i]);
    }

    for(i = 1; i < N; i++)
    {
        max = 1;
        for(j = i - 1; j >= 0; j--)
        {
            if(bridge[i] > bridge[j] && max < rocks[j] + 1)
            {
                max = rocks[j] + 1;
            }
        }
        rocks[i] = max;
    }

    max = rocks[0];
    for(i = 1; i < N; i++)
    {
        if(max < rocks[i])
        {
            max = rocks[i];
        }
    }

    printf("%d", max);

  return 0;
}
