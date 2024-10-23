#include <stdio.h>
#include <stdlib.h>

typedef struct Node
{
    int value;
    struct Node *next;
} Node;

void reverse(Node **head);
Node *recurse(Node *chain);

int main(void)
{
    Node three = {3, NULL};
    Node two = {2, &three};
    Node one = {1, &two};

    Node *walker = &one;
    while (walker != NULL)
    {
        printf("%i\n", walker->value);
        walker = walker->next;
    }

    Node *head = &one;
    reverse(&head);

    walker = &three;
    while (walker != NULL)
    {
        printf("%i\n", walker->value);
        walker = walker->next;
    }
}

void reverse(Node **head)
{
    Node *start = *head;
    Node *chain = recurse(*head);
    while (chain != start)
    {
        chain = chain->next;
    }
    chain->next = NULL;
}

Node *recurse(Node *chain)
{
    if (chain->next == NULL)
    {
        return chain;
    }
    return recurse(chain->next)->next = chain;
}
