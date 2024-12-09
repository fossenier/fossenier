#include <stdio.h>
#include <stdlib.h>

typedef struct Node
{
    int value;
    struct Node *next;
} Node;

void reverse(Node **head);
Node *recurse(Node *chain);
void print(Node *walker);

int main(void)
{
    Node four = {4, NULL};
    Node three = {3, &four};
    Node two = {2, &three};
    Node one = {1, &two};

    Node *head = &one;

    print(head);

    reverse(&head);

    print(head);
}

void reverse(Node **head)
{
    *head = recurse(*head);
}

Node *recurse(Node *current)
{
    if (current->next == NULL)
    {
        return current;
    }
    Node *head = recurse(current->next);
    current->next->next = current;
    current->next = NULL;
    return head;
}

void print(Node *walker)
{
    while (walker != NULL)
    {
        printf("%i\n", walker->value);
        walker = walker->next;
    }
}
