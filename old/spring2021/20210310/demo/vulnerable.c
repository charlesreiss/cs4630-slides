#define _FORTIFY_SOURCE 0
#include <stdio.h>
float vulnerable(FILE *f, int count) {
    float buffer[16];
    if (count >= sizeof(buffer)) {
        return 0.f;
    }
    fread(buffer, count * sizeof(float), 1, f);
    float sum = 0.f, sum2 = 0.f;
    for (int i = 0; i < 16; ++i) {
        sum2 += buffer[i] * buffer[i];
        sum += buffer[i];
    }
    return (sum2 - sum * sum / count) / (count - 1);
}
