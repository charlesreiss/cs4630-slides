#include <stdlib.h>
#include <stdio.h>

__attribute__((noinline))
int get_number() {
    char buffer[100];
    int c;
    int i = 0;
    while ((c = getchar()) != EOF && c != '\n') {
        buffer[i++] = c;
    }
    buffer[i++] = '\0';
    return atoi(buffer);
}

int main(void) {
    printf("The number is %d\n", get_number());
}
