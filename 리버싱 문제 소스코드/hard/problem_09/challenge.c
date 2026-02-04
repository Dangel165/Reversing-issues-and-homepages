#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef struct node {
    int data;
    struct node* next;
} node_t;

node_t* create_list() {
    node_t* head = malloc(sizeof(node_t));
    head->data = 0x46;
    head->next = malloc(sizeof(node_t));
    head->next->data = 0x4C;
    head->next->next = malloc(sizeof(node_t));
    head->next->next->data = 0x41;
    head->next->next->next = malloc(sizeof(node_t));
    head->next->next->next->data = 0x47;
    head->next->next->next->next = NULL;
    return head;
}

int main() {
    char input[10];
    printf("Enter 4 characters: ");
    scanf("%s", input);
    
    node_t* list = create_list();
    node_t* current = list;
    
    int i = 0;
    while (current && i < 4) {
        if (input[i] != current->data) {
            printf("Wrong!\n");
            return 1;
        }
        current = current->next;
        i++;
    }
    
    if (i == 4) {
        printf("FLAG{linked_list_traversal}\n");
    }
    
    return 0;
}