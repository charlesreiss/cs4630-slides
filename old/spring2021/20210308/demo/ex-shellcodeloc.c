#include <stdio.h>

void getInitials(char *init) {
    char first[50]; char second[50];
    scanf("%s%s", first, second);
    init[0] = first[0];
    init[1] = second[0];
}

int main() {
    char initials[2];
    getInitials(initials);
    printf("%c%c\n", initials[0], initials[1]);
    return 0;
}
