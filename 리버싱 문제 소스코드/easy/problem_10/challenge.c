#include <stdio.h>

int main() {
    int input;
    printf("Guess the number (1-10): ");
    scanf("%d", &input);
    
    int secret = 7;
    
    if (input == secret) {
        printf("FLAG{lucky_number_seven}\n");
    } else {
        printf("Wrong guess!\n");
    }
    
    return 0;
}