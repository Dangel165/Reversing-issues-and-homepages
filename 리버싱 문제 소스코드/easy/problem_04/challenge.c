#include <stdio.h>
#include <string.h>

int main() {
    char input[50];
    printf("What's the magic word? ");
    scanf("%s", input);
    
    if (strlen(input) == 7 && input[0] == 'r' && input[6] == 'e') {
        printf("FLAG{reverse_engineering}\n");
    } else {
        printf("Not quite right!\n");
    }
    
    return 0;
}