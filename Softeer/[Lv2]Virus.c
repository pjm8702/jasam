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
