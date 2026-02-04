#include <stdio.h>
#include <string.h>

int validate_key(char* key) {
    if (strlen(key) != 8) return 0;
    
    int sum = 0;
    for (int i = 0; i < 8; i++) {
        sum += key[i] * (i + 1);
    }
    
    return sum == 2856;
}

int main() {
    char input[50];
    printf("Enter the license key: ");
    scanf("%s", input);
    
    if (validate_key(input)) {
        printf("FLAG{license_validation_bypassed}\n");
    } else {
        printf("Invalid license key!\n");
    }
    
    return 0;
}