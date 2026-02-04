#include <stdio.h>

int fibonacci(int n) {
    if (n <= 1) return n;
    return fibonacci(n-1) + fibonacci(n-2);
}

int main() {
    int input;
    printf("Enter a number: ");
    scanf("%d", &input);
    
    if (fibonacci(input) == 55) {
        printf("FLAG{fibonacci_sequence_master}\n");
    } else {
        printf("Not the right fibonacci number!\n");
    }
    
    return 0;
}