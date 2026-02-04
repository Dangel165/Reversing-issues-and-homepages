#include <stdio.h>
#include <string.h>

void vm_execute(char* bytecode, int len) {
    int stack[100] = {0};
    int sp = 0;
    int pc = 0;
    
    while (pc < len) {
        switch (bytecode[pc]) {
            case 0x01:
                stack[sp++] = bytecode[pc + 1];
                pc += 2;
                break;
            case 0x02:
                stack[sp - 2] += stack[sp - 1];
                sp--;
                pc++;
                break;
            case 0x03:
                if (stack[--sp] == 100) {
                    printf("FLAG{virtual_machine_cracked}\n");
                }
                pc++;
                break;
            default:
                pc++;
        }
    }
}

int main() {
    int input;
    printf("Enter a number: ");
    scanf("%d", &input);
    
    char bytecode[] = {0x01, 0x1E, 0x01, 0x32, 0x02, 0x03};
    
    if (input == 30) {
        vm_execute(bytecode, 6);
    } else {
        printf("Wrong input!\n");
    }
    
    return 0;
}