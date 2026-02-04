#include <stdio.h>
#include <string.h>

int checksum(char* str) {
    int sum = 0;
    for (int i = 0; i < strlen(str); i++) {
        sum += str[i];
    }
    return sum;
}

int main() {
    char input[50];
    printf("Enter the key: ");
    scanf("%s", input);
    
    if (checksum(input) == 532) {
        printf("FLAG{checksum_validation_passed}\n");
    } else {
        printf("Invalid key!\n");
    }
    
    return 0;
}