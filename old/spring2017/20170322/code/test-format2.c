#include <stdlib.h>
#include <stdio.h>

int exploited() {
    fprintf(stderr, "\nGot here!\n");
    exit(0);
}

int main(void) {
    char buffer[100];
    while (fgets(buffer, sizeof buffer, stdin)) {
        printf(buffer);
    }
}
