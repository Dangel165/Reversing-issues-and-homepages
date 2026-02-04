#include <stdio.h>
#include <string.h>

unsigned int crc32(const char* data, size_t length) {
    unsigned int crc = 0xFFFFFFFF;
    for (size_t i = 0; i < length; i++) {
        crc ^= data[i];
        for (int j = 0; j < 8; j++) {
            if (crc & 1) {
                crc = (crc >> 1) ^ 0xEDB88320;
            } else {
                crc >>= 1;
            }
        }
    }
    return ~crc;
}

int main() {
    char input[100];
    printf("Enter the key: ");
    scanf("%s", input);
    
    if (crc32(input, strlen(input)) == 0x414fa339) {
        printf("FLAG{crc32_checksum_cracked}\n");
    } else {
        printf("Invalid key!\n");
    }
    
    return 0;
}