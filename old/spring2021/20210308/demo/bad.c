__attribute__((noinline))
int vulnerable(void) {
    char buffer[10];
    gets(buffer);
}

int main(void){
    vulnerable();
}
