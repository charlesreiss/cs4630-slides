#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <limits.h>
#include <string.h>
#include <errno.h>

#include <curl/curl.h>
int main() {
    printf("here\n");
#if 0
    FILE *fh = fopen("output.txt", "w");
    fprintf(fh, "example");
    fclose(fh);
#endif
    CURL *handle = curl_easy_init();
    if (CURLE_OK != curl_easy_setopt(handle, CURLOPT_URL, "https://www.cs.virginia.edu/~cr4bd/test.txt")) abort();
    if (CURLE_OK != curl_easy_perform(handle)) abort();
}

