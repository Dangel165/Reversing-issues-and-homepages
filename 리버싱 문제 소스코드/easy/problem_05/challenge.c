#include <stdio.h>

int main() {
    int x = 15;
    int y = 25;
    int input;
    
    printf("What is x * y? ");
    scanf("%d", &input);
    
    if (input == x * y) {
        printf("FLAG{multiplication_master}\n");
    } else {
        printf("Wrong calculation!\n");
    }
    
    return 0;
}