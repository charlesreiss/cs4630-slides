#include <stdlib.h>
#include <stdio.h>

int read_number() {
    char buffer[20];
    int ch; unsigned i = 0;
    while (1) {
        ch = getchar();
        if (ch == '\n' || ch == EOF) break;
        buffer[i] = ch;
        i += 1;
    }
    buffer[i] = '\0';
    return atoi(buffer);
}
