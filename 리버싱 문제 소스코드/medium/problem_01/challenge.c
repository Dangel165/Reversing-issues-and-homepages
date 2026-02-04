#include <stdio.h>
#include <string.h>

void decrypt(char* str) {
    for (int i = 0; i < strlen(str); i++) {
        str[i] = str[i] - 1;
    }
}

int main() {
    char input[50];
    
    printf("Enter the password: ");
    scanf("%s", input);
    
    decrypt(input);
    
    if (strcmp(input, "password") == 0) {
        printf("FLAG{caesar_cipher_decoded}\n");
    } else {
        printf("Wrong password!\n");
    }
    
    return 0;
}