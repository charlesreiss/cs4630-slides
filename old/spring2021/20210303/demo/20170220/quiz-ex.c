#include <stdio.h>

struct QuizQuestion {
    const char *question;
    const char *answer;
};

#define NUM_QUESTIONS 10

struct QuizQuestion questions[NUM_QUESTIONS];
int checkAnswer(const char *answer, struct QuizQuestion *question);

int giveQuiz() {
    volatile int score = 0;
    char buffer[100];
    for (int i = 0; i < NUM_QUESTIONS; ++i) {
        gets(buffer);
        if (checkAnswer(buffer, &questions[i])) {
            score += 1;
        }
    }
    return score;
}
