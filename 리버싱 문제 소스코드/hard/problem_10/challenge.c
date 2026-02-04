#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void self_modify() {
    static int modified = 0;
    if (!modified) {
        modified = 1;
    }
}

int recursive_hash(char* str, int depth) {
    if (depth == 0 || *str == '\0') {
        return 0;
    }
    
    return (*str * depth) + recursive_hash(str + 1, depth - 1);
}

int main() {
    self_modify();
    
    char input[20];
    printf("Enter the master key: ");
    scanf("%s", input);
    
    int hash_result = recursive_hash(input, strlen(input));
    
    if (hash_result == 1337 && strlen(input) == 8) {
        printf("FLAG{self_modifying_recursive_hash}\n");
    } else {
        printf("Hash verification failed!\n");
    }
    
    return 0;
}