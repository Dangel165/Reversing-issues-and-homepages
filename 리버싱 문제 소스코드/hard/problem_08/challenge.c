#include <stdio.h>
#include <string.h>
#include <time.h>

int time_based_check() {
    time_t current_time = time(NULL);
    return (current_time % 1000) < 500;
}

void polymorphic_decrypt(char* data, int key) {
    for (int i = 0; i < strlen(data); i++) {
        data[i] = ((data[i] ^ key) - i) & 0xFF;
    }
}

int main() {
    char input[50];
    printf("Enter the code: ");
    scanf("%s", input);
    
    if (!time_based_check()) {
        printf("Time window expired!\n");
        return 1;
    }
    
    polymorphic_decrypt(input, 0x42);
    
    if (strcmp(input, "secret") == 0) {
        printf("FLAG{polymorphic_time_based_check}\n");
    } else {
        printf("Decryption failed!\n");
    }
    
    return 0;
}