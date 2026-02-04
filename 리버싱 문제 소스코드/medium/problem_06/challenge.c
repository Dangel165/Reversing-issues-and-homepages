#include <stdio.h>

int is_prime(int n) {
    if (n < 2) return 0;
    for (int i = 2; i * i <= n; i++) {
        if (n % i == 0) return 0;
    }
    return 1;
}

int main() {
    int input;
    printf("Enter a prime number: ");
    scanf("%d", &input);
    
    if (is_prime(input) && input > 100 && input < 200) {
        printf("FLAG{prime_number_in_range}\n");
    } else {
        printf("Not a prime in the specified range!\n");
    }
    
    return 0;
}