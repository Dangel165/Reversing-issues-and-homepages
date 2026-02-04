#include <stdio.h>
#include <string.h>

void obfuscated_check(char* input) {
    char target[] = {0x48, 0x65, 0x6c, 0x6c, 0x6f};
    int len = strlen(input);
    
    for (int i = 0; i < len; i++) {
        input[i] = ((input[i] ^ 0xAA) + 0x10) & 0xFF;
    }
    
    if (len == 5 && memcmp(input, target, 5) == 0) {
        printf("FLAG{obfuscated_string_manipulation}\n");
    } else {
        printf("Wrong input!\n");
    }
}

int main() {
    char input[50];
    printf("Enter the code: ");
    scanf("%s", input);
    
    obfuscated_check(input);
    return 0;
}