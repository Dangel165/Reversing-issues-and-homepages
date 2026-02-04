#include <stdio.h>

int main() {
    int input;
    printf("Enter a number: ");
    scanf("%d", &input);
    
    if (input == 42) {
        printf("FLAG{the_answer_to_everything}\n");
    } else {
        printf("Try again!\n");
    }
    
    return 0;
}