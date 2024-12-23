#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void read_until_newline() {
    char c;
    do {
        c = getchar();
    } while (c != EOF && c != '\n');
}

void read_command(char *command, char *arg) {
    char line[100];
    fgets(line, sizeof line, stdin);
    sscanf(line, "%s%s", command, arg);
}


int *data;
long data_size;
void prompting_loop() {
    unsigned long current_index;
    for (;;) {
        char command[100]; char arg[100];
        read_command(command, arg);
        if (0 == strcmp(command, "show")) {
            printf("current_index = %lu\n", current_index);
            if (current_index < data_size)
                printf("value at index = %d\n", data[current_index]);
            else
                printf("index out of range\n");
        } else if (0 == strcmp(command, "input")) {
            int index; long value;
            sscanf(arg, "%d,%ld", &index, &value);
            data = realloc(data, sizeof(int) * (index + 1));
            data[index] = value;
            current_index = index;
        } else if (0 == strcmp(command, "exit")) {
            return;
        }
    }
}

void process_input(FILE *f) {
    data_size = 0;
    fscanf(f, "%ld", &data_size);
}

int main() {
    FILE *input = fopen("input.txt", "r");
    FILE *output = fopen("output.txt", "w");
    process_input(input);
    prompting_loop();
    if (data)
        fprintf(output, "%d\n", data[0]);
    return 0;
}

