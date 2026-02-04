#include <stdio.h>
#include <string.h>

int main() {
    char input[100];
    char flag[] = "FLAG{simple_string_comparison}";
    
    printf("Enter the password: ");
    scanf("%s", input);
    
    if (strcmp(input, "password123") == 0) {
        printf("Correct! Flag: %s\n", flag);
    } else {
        printf("Wrong password!\n");
    }
    
    return 0;
}