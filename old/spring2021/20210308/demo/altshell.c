#include <stdio.h>
#include <string.h>
char current_student[200];
int GetAndCompareAnswer(char *question,
                        char *expected_answer) {
       char answer[100];
       scanf("%[a-zA-Z0-9 \t\n]", answer);
       return strcmp(answer, expected_answer) == 0;
}

int main() {
    fgets(current_student, sizeof current_student, stdin);
    printf("student = %s\n", current_student);
    return GetAndCompareAnswer("foo" ,"bar");
}
