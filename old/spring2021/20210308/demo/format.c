#define _FORTIFY_SOURCE 0
#include <stdlib.h>
#include <stdio.h>

int exploited() {
    printf("\n\nGot here!\n");
    exit(0);
}

int main(void) {
    char buffer[100];
    while (fgets(buffer, sizeof buffer, stdin)) {
        printf(buffer);
    }
}
