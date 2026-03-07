#include <stdio.h>
extern char *gets(char *);

void vulnerable() {
    char str[128];
    printf("Input: "); fflush(stdout);
    gets(str);
}

int main() {vulnerable();}
