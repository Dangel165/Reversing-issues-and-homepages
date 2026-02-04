#include <stdio.h>

int main() {
    int arr[] = {1, 3, 5, 7, 9};
    int input;
    
    printf("Enter an odd number between 1 and 10: ");
    scanf("%d", &input);
    
    for (int i = 0; i < 5; i++) {
        if (arr[i] == input) {
            printf("FLAG{array_search_success}\n");
            return 0;
        }
    }
    
    printf("Not found in array!\n");
    return 0;
}