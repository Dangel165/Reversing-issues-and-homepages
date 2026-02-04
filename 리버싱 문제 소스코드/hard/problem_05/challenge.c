#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void decrypt_flag(char* key) {
    unsigned char encrypted[] = {0x1a, 0x0e, 0x00, 0x06, 0x7b, 0x0c, 0x19, 0x1f, 0x0a, 0x1c, 0x1c, 0x04, 0x18, 0x09, 0x5f, 0x0c, 0x19, 0x1f, 0x0a, 0x1c, 0x1c, 0x04, 0x18, 0x09, 0x7d};
    
    if (strlen(key) != 8) return;
    
    for (int i = 0; i < 25; i++) {
        encrypted[i] ^= key[i % 8];
    }
    
    printf("%s\n", encrypted);
}

int validate_key(char* key) {
    int checksum = 0;
    for (int i = 0; i < strlen(key); i++) {
        checksum += key[i] * (i * i + 1);
    }
    return checksum == 25140;
}

int main() {
    char input[50];
    printf("Enter the decryption key: ");
    scanf("%s", input);
    
    if (validate_key(input)) {
        decrypt_flag(input);
    } else {
        printf("Invalid key!\n");
    }
    
    return 0;
}