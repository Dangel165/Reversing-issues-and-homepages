#include <stdio.h>
#include <string.h>

void xor_encrypt(char* str, char key) {
    for (int i = 0; i < strlen(str); i++) {
        str[i] ^= key;
    }
}

int main() {
    char input[50];
    char target[] = {0x1f, 0x0a, 0x1c, 0x1c, 0x04, 0x18, 0x09, 0x00};
    
    printf("Enter the password: ");
    scanf("%s", input);
    
    xor_encrypt(input, 0x42);
    
    if (memcmp(input, target, 8) == 0) {
        printf("FLAG{xor_encryption_cracked}\n");
    } else {
        printf("Wrong password!\n");
    }
    
    return 0;
}