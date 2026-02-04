#include <stdio.h>
#include <string.h>

int main() {
    char input[100];
    printf("Enter serial: ");
    scanf("%s", input);
    
    if (strlen(input) != 16) {
        printf("Wrong length!\n");
        return 1;
    }
    
    int sum1 = 0, sum2 = 0;
    for (int i = 0; i < 8; i++) {
        sum1 += input[i];
        sum2 += input[i + 8];
    }
    
    if (sum1 == 520 && sum2 == 584) {
        int product = 1;
        for (int i = 0; i < 16; i += 2) {
            product *= (input[i] - '0');
        }
        
        if (product == 0) {
            printf("FLAG{complex_serial_validation}\n");
        } else {
            printf("Serial validation failed!\n");
        }
    } else {
        printf("Checksum mismatch!\n");
    }
    
    return 0;
}