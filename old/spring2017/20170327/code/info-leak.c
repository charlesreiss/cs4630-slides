#include <stdio.h>
#include <string.h>
#include <stdlib.h>
void informationLeak() {
    char buffer[32];
    char command[32];
    while (fgets(command, sizeof command, stdin)) {
        if (!strcmp(command, "!show\n")) {
            printf("%s", buffer);
        } else {
            strcpy(command, buffer);
        }
    }
}

int main(void) {
    printf("Starting\n");
    informationLeak();
}
