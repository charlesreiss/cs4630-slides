int array[1024] = {1,2,3};
int foo(int x) {
    return array[54];
}

int main(int argc, char **argv) {
    return foo(argc);
}
