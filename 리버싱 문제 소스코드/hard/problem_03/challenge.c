#include <stdio.h>
#include <string.h>

void anti_debug() {
    volatile int x = 0;
    for (int i = 0; i < 1000000; i++) {
        x += i;
    }
}

int main() {
    anti_debug();
    
    char input[50];
    printf("Enter password: ");
    scanf("%s", input);
    
    char encoded[] = {0x72, 0x65, 0x76, 0x65, 0x72, 0x73, 0x65};
    
    for (int i = 0; i < 7; i++) {
        if (input[i] != encoded[i]) {
            printf("Wrong!\n");
            return 1;
        }
    }
    
    if (strlen(input) == 7) {
        printf("FLAG{anti_debug_bypassed}\n");
    } else {
        printf("Wrong length!\n");
    }
    
    return 0;
}