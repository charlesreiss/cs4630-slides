struct Canvas;

class Shape {
public:
    virtual void draw(Canvas *c) = 0;
};

class Polygon : public Shape {
public:
    virtual void draw(Canvas *c) {}
    //virtual ~Polygon() {}
};

int main(void) {
    Shape *s = new Polygon;
    s->draw(0);
    delete s;
}
