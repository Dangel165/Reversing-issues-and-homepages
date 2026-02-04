#include <stdio.h>

int mystery_function(int n) {
    int result = 1;
    for (int i = 1; i <= n; i++) {
        result *= i;
    }
    return result;
}

int main() {
    int input;
    printf("Enter a number: ");
    scanf("%d", &input);
    
    if (mystery_function(input) == 120) {
        printf("FLAG{factorial_function_identified}\n");
    } else {
        printf("Wrong number!\n");
    }
    
    return 0;
}