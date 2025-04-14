#include <string.h>
extern char *attacker_controlled;
extern int len;
int vulnerable() {
    char buffer[42];
    memcpy(buffer, attacker_controlled, len);
}
