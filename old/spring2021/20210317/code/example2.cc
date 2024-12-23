struct Foo {
    virtual const char *bar() { return "Foo::bar"; }
};

int main() {
    Foo *f = new Foo;
    f->bar();
}
