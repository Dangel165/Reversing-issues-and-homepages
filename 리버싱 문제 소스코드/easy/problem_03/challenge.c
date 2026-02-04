#include <stdio.h>

int main() {
    int a, b;
    printf("Enter two numbers: ");
    scanf("%d %d", &a, &b);
    
    if (a + b == 100) {
        printf("FLAG{math_is_easy}\n");
    } else {
        printf("Wrong sum!\n");
    }
    
    return 0;
}