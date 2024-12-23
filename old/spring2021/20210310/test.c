#include <stdio.h>
#include <stdlib.h>

    void ReadAndProcess(FILE *in) {
        unsigned int size;
        unsigned long tag;
        int data[1000];
        fread(&size, 4, 1, in);
        unsigned int data_count = size / sizeof(int);
        if (data_count > 1000){
            fprintf(stderr, "TOO BIG!\n");
            abort();
        } else {
            fread(&tag, 8, 1, in);
            fread(&data[0], size - 8, 1, in);
            DoSomethingWith(tag, data, data_count);
        }
    }
