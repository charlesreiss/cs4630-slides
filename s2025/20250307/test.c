#include <stdio.h>
void getInitials(char *init) {
    char first[50]; char second[50];
    scanf("%s%s", first, second);
    init[0] = first[0];
    init[1] = second[0];
    printf("[%s][%s]\n", first, second);
}


int main() {
    char buf[10];
    getInitials(buf);
}
