#include <node.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    node *head = NULL;
    map_add(&head, "one", 1);
    map_add(&head, "two", 2);
    map_add(&head, "three", 3);
    map_add(&head, "four", 4);
    map_add(&head, "five", 5);
    map_print(head);
    map_remove(&head, "three");
    map_print(head);
    map_update(head, "four", 44);
    map_print(head);
    map_update(head, "six", 6);
    map_print(head);
    return 0;
}

// map_add
int map_add(node **head, const char *new_key, const int new_value)
{
    // Dereference head, and assign it to a walker
    node *walker = *head;
    // Track the last node seen (initially null)
    node *last_node = NULL;

    // Try to walk to the end of the list
    while (walker != NULL)
    {
        // Stop if the key is in the chain, and just update that node
        if (strncmp(walker->key, new_key, KEY_LEN) == 0)
        {
            // Assign the new value, and return early
            walker->value = new_value;
            return 0;
        }
        // Update the walker + last node to go down the chain
        last_node = walker;
        walker = walker->next;
    }
    // Post Condition: the key is not in the chain, walker = NULL

    // Allocate a new node
    // Basically, give me a memory adress of a place that I can use as a node
    node *new_node = malloc(sizeof(node));
    // If null, return -1 (error!)
    if (new_node == NULL)
    {
        return -1;
    }
    // Copy the key, remember! strncpy and strncmp (old, new, size)
    strncpy(new_node->key, new_key, KEY_LEN);
    // Set the value
    new_node->value = new_value;
    // It is the end, point it to nothing
    new_node->next = NULL;

    // If last node is also, null, there never was a first node
    if (last_node == NULL)
    {
        // Set the DEREFERENCED head to point to this new chain (the start)
        *head = new_node;
    }
    // Otherwise, there is a chain to add to
    else
    {
        // Point the last node to this new node
        last_node->next = new_node;
    }

    // Return success
    return 0;
}

// map_remove
int map_remove(node **head, const char *target_key)
{
    // Dereference head, and set it as our walker
    node *walker = *head;
    // Track the last node seen (initially null)
    node *last_node = NULL;

    // Try and walk to the end of the list
    while (walker != NULL)
    {
        // Stop when we find the target key
        if (strncmp(walker->key, target_key, KEY_LEN) == 0)
        {
            break;
        }
        // Walky walky
        last_node = walker;
        walker = walker->next;
    }
    // Post condition, walker is null (key not found) or it is the target node
    if (walker == NULL)
    {
        // Fail, key not found
        return -1;
    }
    if (last_node == NULL)
    {
        // There never was a prior node, so reattach the head DEREFERENCED to next
        *head = walker->next;
    }
    else
    {
        // There was a last node, glue it to the walker's next (even if that is the end)
        last_node->next = walker->next;
    }
    // Free the walker baby
    free(walker);
    return 0;
}

// map_update
int map_update(node *head, const char *target_key, const int new_value)
{
    // Set the walker to the DEREFERENCED head
    node *walker = head;
    // Try and walk to the end
    while (walker != NULL)
    {
        // Spot matching keys
        if (strncmp(walker->key, target_key, KEY_LEN) == 0)
        {
            // Update the value
            walker->value = new_value;
            return 0;
        }
        // Walky walky
        walker = walker->next;
    }
    // Failure on key not found
    return -1;
}

// map_find
node *map_find(node *head, const char *search_key)
{
    // Set the walker to the head
    node *walker = head;
    // Try and walk to the end
    while (walker != NULL)
    {
        // Spot matching keys
        if (strncmp(walker->key, search_key, KEY_LEN) == 0)
        {
            // Return the walker
            return walker;
        }
        // Walky walky
        walker = walker->next;
    }
    // Key not found
    return NULL;
}

// map_print
void map_print(node *head)
{
    // Set the walker to the head
    node *walker = head;
    // Try and walk to the end
    while (walker != NULL)
    {
        // Print the key and value
        printf("%s: %i\n", walker->key, walker->value);
        // Walky walky
        walker = walker->next;
    }
}
