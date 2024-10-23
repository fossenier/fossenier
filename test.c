#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    char *target = malloc(2 * sizeof(char));
    target[0] = 104;
    target[1] = '\0';

    target[0]++;

    printf("%s\n", target);

    free(target);
}
