#include <iostream>

__attribute__((noinline))
void do_something_with(long *array) {
        __asm__ volatile("" :: "a"(array) : "memory");
}

void vulnerable(long value, int offset) {
    long array[10] = {1,2,3,4,5,6,7,8,9,10};
    array[offset] = value;
    do_something_with(array);
}

int main() {
    long value; int offset;
    std::cin >> std::hex >> value >> offset;
    vulnerable(value, offset);
}
