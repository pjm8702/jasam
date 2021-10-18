/*
N명의 학생들의 성적이 학번순서대로 주어졌다. 학번 구간 [A, B]가 주어졌을 때 이 학생들 성적의 평균을 구하는 프로그램을 작성하라.

[입력형식]
첫 번째 줄에 학생 수 N과 구간 수 K가 주어진다. 두 번째 줄에는 학생의 성적 Si (1 ≤ i ≤ N)가 주어진다. i + 2 (1 ≤ i ≤ K)번째 줄에는 i번째 구간 Ai, Bi가 주어진다.

입력은 다음 조건을 만족한다.
    1 ≤ N ≤ 106 인 정수
    1 ≤ K ≤ 104 인 정수
    1 ≤ Si ≤ 100 인 정수
    1 ≤ Ai ≤ Bi ≤ N

[출력형식]
i번째 줄에 i번째 구간의 성적평균(소수셋째자리에서 반올림)을 출력한다.
(차이가 0.01이하이면 정답으로 채점됨)

[입력예제]
5 3
10 50 20 70 100
1 3
3 4
1 5

[출력예제]
26.67
45.00
50.00
*/

#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int N, K, S, A, B;
    int i;
    double *sum;
    double avg;
    
    scanf("%d %d", &N, &K);
    sum = (double*)calloc(N+1, sizeof(double));
    scanf("%d", &S);
    sum[1] = S;
    for(i = 2; i <= N; i++)
    {
        scanf("%d", &S);
        sum[i] = sum[i-1] + S;
    }

    for(i = 0; i < K; i++)
    {
        scanf("%d %d\n", &A, &B);
        avg = (sum[B] - sum[A-1]) / (B - A + 1);
        printf("%.2lf\n", avg);
    }
    
    free(sum);
    
  return 0;
}
