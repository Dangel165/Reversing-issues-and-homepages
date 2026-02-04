#include <stdio.h>

int calculate(int a, int b, int c) {
    return (a << 2) + (b >> 1) - c;
}

int main() {
    int x, y, z;
    printf("Enter three numbers: ");
    scanf("%d %d %d", &x, &y, &z);
    
    if (calculate(x, y, z) == 42) {
        printf("FLAG{bitwise_operations_master}\n");
    } else {
        printf("Wrong calculation!\n");
    }
    
    return 0;
}