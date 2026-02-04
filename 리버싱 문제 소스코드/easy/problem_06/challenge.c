#include <stdio.h>

int main() {
    char c;
    printf("Enter a character: ");
    scanf("%c", &c);
    
    if (c >= 'A' && c <= 'Z') {
        printf("FLAG{uppercase_letter}\n");
    } else {
        printf("Not an uppercase letter!\n");
    }
    
    return 0;
}