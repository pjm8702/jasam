/*
루팡은 배낭을 하나 메고 은행금고에 들어왔다. 금고 안에는 값비싼 금, 은, 백금 등의 귀금속 덩어리가 잔뜩 들어있다.
배낭은 W ㎏까지 담을 수 있다. 각 금속의 무게와 무게당 가격이 주어졌을 때 배낭을 채울 수 있는 가장 값비싼 가격은 얼마인가?
루팡은 전동톱을 가지고 있으며 귀금속은 톱으로 자르면 잘려진 부분의 무게만큼 가치를 가진다.

[입력형식]
첫 번째 줄에 배낭의 무게 W와 귀금속의 종류 N이 주어진다. i + 1 (1 ≤ i ≤ N)번째 줄에는 i번째 금속의 무게 Mi와 무게당 가격 Pi가 주어진다.

입력은 다음 조건을 만족한다.
    1 ≤ N ≤ 106 인 정수
    1 ≤ W ≤ 104 인 정수
    1 ≤ Mi, Pi ≤ 104 인 정수

[출력형식]
첫 번째 줄에 배낭에 담을 수 있는 가장 비싼 가격을 출력하라.

[입력예제]
100 2
90 1
70 2

[출력예제]
170
*/

#include <stdio.h>
#include <stdlib.h>

typedef struct
{
    int weight;
    int price;
} Jewel;

int main(void)
{
    int W, N;
    int i, idx = 0;
    Jewel *jewel;
    int table[10001] = {0,};
    int curWeight = 0, price = 0;

    scanf("%d %d", &W, &N);
    jewel = (Jewel*)calloc(N, sizeof(Jewel));
    for(i = 0; i < N; i++)
    {
        scanf("%d %d", &(jewel[i].weight), &(jewel[i].price));
        table[jewel[i].price] += jewel[i].weight;
    }

    curWeight = W;
    for(i = 10000; i > 0; i--)
    {
        if(table[i] != 0)
        {
            if(curWeight >= table[i])
            {
                price += table[i] * i;
            }
            else
            {
                price += curWeight * i;
                break;
            }

            curWeight -= table[i];
        }
    }

    printf("%d\n", price);

    free(jewel);

  return 0;
}
