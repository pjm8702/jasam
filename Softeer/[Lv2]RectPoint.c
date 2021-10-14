/*
0 0 | 0 0 0 | 0 0 0 0 0
0 0 | 0 0 0 | 0 0 0 0 0
    | 0 0 0 | 0 0 0 0 0
    |       | 0 0 0 0 0
    |       | 0 0 0 0 0
    
0단계 : 사각형 점 개수 4개
1단계 : 사각형 점 개수 9개
2단계 : 사각형 점 개수 25개

첫째 줄에 N(1 ≤ N ≤ 15)이 주어졌을 때 사각형 점의 개수 계산하기
*/

#include <stdio.h>


int main(void)
{
    int N, i;
    int point = 2;
    int add = 1;

    scanf("%d", &N);
    for(i = 0; i < N; i++)
    {
        point = point + add;
        add *= 2;
    }

    printf("%d\n", point * point);

    return 0;
}
