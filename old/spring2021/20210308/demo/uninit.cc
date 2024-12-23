#include <iostream>
#include <string>
using std::cin; using std::cout; using std::string; using std::endl;

__attribute__((noinline))
void do_something_with(int *x) {
    asm volatile("");
}

string command;
void vulnerable(){
    int value;
    for (;;) {
        cin >> command;
        if (command == "set") {
            cin >> value;
        } else if (command == "get") {
            cout << value << endl;
        } else if (command == "exit") {
            break;
        }
    }
}

void leak() {
    int secrets[] = {
        12345678, 23456789, 34567890,
        45678901, 56789012, 67890123,
    };
    cout << (void*) secrets << endl;
    do_something_with(secrets);
}

int main() {
    leak();
    vulnerable();
}

