struct Foo {
    virtual const char *bar();
    virtual ~Foo() {}
};

struct Baz : Foo {
    virtual const char *bar() override;
};

const char *Foo::bar() { return "Foo::bar"; }
const char *Baz::bar() { return "Baz::bar"; }
