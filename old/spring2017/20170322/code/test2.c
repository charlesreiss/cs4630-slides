int foo(int n) {
    switch (n) {
    case 0:
    case 2:
    case 4:
        return 1;
    case 1:
    case 3:
    case 5:
        return 2;
    default:
        return 3;
    }
}

