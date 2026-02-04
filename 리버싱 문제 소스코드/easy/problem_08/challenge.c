#include <stdio.h>

int main() {
    int input;
    printf("Enter a number: ");
    scanf("%d", &input);
    
    if (input % 2 == 0 && input > 0) {
        printf("FLAG{even_positive_number}\n");
    } else {
        printf("Not an even positive number!\n");
    }
    
    return 0;
}