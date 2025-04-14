#include <stdio.h>

int vulnerable() {
    char buffer[100];
    gets(buffer);
}


int main(void) {
    vulnerable();
}
