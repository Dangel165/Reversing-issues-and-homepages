#include <stdio.h>
#include <string.h>

void reverse_string(char* str) {
    int len = strlen(str);
    for (int i = 0; i < len / 2; i++) {
        char temp = str[i];
        str[i] = str[len - 1 - i];
        str[len - 1 - i] = temp;
    }
}

int main() {
    char input[50];
    printf("Enter the code: ");
    scanf("%s", input);
    
    reverse_string(input);
    
    if (strcmp(input, "reverse") == 0) {
        printf("FLAG{string_reversal_success}\n");
    } else {
        printf("Wrong code!\n");
    }
    
    return 0;
}