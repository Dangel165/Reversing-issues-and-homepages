#include <stdio.h>

int transform(int x) {
    return (x * 3 + 7) % 256;
}

int main() {
    int input;
    printf("Enter a number: ");
    scanf("%d", &input);
    
    int result = transform(input);
    
    if (result == 100) {
        printf("FLAG{mathematical_transformation}\n");
    } else {
        printf("Wrong transformation result!\n");
    }
    
    return 0;
}