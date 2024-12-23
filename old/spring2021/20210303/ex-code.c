#define _XOPEN_SOURCE 700L
#include <stdio.h>
extern char *gets(char *);
extern int GradeAnswer(char *, int);
extern int Process(int*);
void GradeAssignment(FILE *in) {
    int question_score[10];
    char buffer[16];
    for (int i = 0; i < 10; ++i) {
        gets(buffer);
        question_score[i] = GradeAnswer(buffer, i);
    }
    Process(question_score);
}
