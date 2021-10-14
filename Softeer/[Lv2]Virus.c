/*
[Lv2]Virus.c
바이러스가 숙주의 몸속에서 1초당 P배씩 증가한다. 처음에 바이러스 K마리가 있었다면 N초 후에는 총 몇 마리의 바이러스로 불어날까? N초 동안 죽는 바이러스는 없다고 가정한다.

[입력형식] 
첫 번째 줄에 처음 바이러스의 수 K, 증가율 P, 총 시간 N(초)이 주어진다. 입력은 다음 조건을 만족한다. 1 ≤ K ≤ 108 인 정수 1 ≤ P ≤ 108 인 정수 1 ≤ N ≤ 106 인 정수

[출력형식] 
최종 바이러스 개수를 1000000007로 나눈 나머지를 출력하라.

[입력예제]
2 3 2

[출력예제]
18
*/

#include <stdio.h>


int main(void)
{
    long long K, P, N;
    int i;
    long long virus = 0;
    scanf("%d %d %d", &K, &P, &N);

    virus = K;
    for(i = 0; i < N; i++)
    {
        virus *= P;
        virus %= 1000000007;
    }
    printf("%ld\n", virus);
  
  return 0;
}
