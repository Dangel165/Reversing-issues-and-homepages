#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef struct {
    int (*validate)(char*);
    char* flag;
} validator_t;

int complex_validate(char* input) {
    int hash = 5381;
    for (int i = 0; input[i]; i++) {
        hash = ((hash << 5) + hash) + input[i];
    }
    return hash == 0x7c967e3f;
}

int main() {
    validator_t v = {complex_validate, "FLAG{djb2_hash_algorithm}"};
    
    char input[100];
    printf("Enter the secret: ");
    scanf("%s", input);
    
    if (v.validate(input)) {
        printf("%s\n", v.flag);
    } else {
        printf("Access denied!\n");
    }
    
    return 0;
}