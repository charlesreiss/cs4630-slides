extern int func1(char *a, int *b);
extern int func2(char *a, int *b);

int example() {
    char buf1[50];
    char buf2[50];
    int result = 0;
    func1(buf1, &result);
    func2(buf2, &result);
    func1(buf1, &result);
    return result;
}
