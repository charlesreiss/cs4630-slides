struct Foo {
    virtual const char *bar();
    virtual ~Foo() {}
};

struct Baz : Foo {
    virtual const char *bar() override;
};

int main() {
    Baz *b = new Baz;
    Foo *f = b;
    f->bar();
}
