#ifndef NODE_H
#define NODE_H

#define KEY_LEN 64

typedef struct node
{
    char key[KEY_LEN];
    int value;
    struct node *next;
} node;

int map_add(node **head, const char *new_key, const int new_value);
int map_remove(node **head, const char *target_key);
int map_update(node *head, const char *target_key, const int new_value);
node *map_find(node *head, const char *search_key);
void map_print(node *head);

#endif
