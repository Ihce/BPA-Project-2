// #include <stdio.h>
// int test() {
//     for(int i = 0; i<10; i++) {
//         printf("%d", i);
//     }
// }
// int main()
// {
//     for(int i = 0; i<10; i++) {
//         printf("%d", i);
//     }

//     test();
// }
// Print numbers from 1 to 10
#include <stdio.h>

int loop(int i) {
    {
        printf("Hello %d", i);
    }
}
int main() {
  for (int i = 1; i < 11; i++) {
    loop(i);
  }
}