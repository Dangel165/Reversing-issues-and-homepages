#include <stdio.h>
#include <string.h>

int main() {
    char input[20];
    printf("Enter your name: ");
    scanf("%s", input);
    
    if (strcmp(input, "admin") == 0) {
        printf("FLAG{admin_access_granted}\n");
    } else if (strcmp(input, "user") == 0) {
        printf("Regular user access\n");
    } else {
        printf("Access denied!\n");
    }
    
    return 0;
}