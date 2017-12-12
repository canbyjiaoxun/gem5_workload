#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(){
    int rand_number; 
    srand(time(NULL));
    //rand_number = rand() % 1000000;
    rand_number = rand() % 200000;
    FILE *rand_file = fopen("rand_seed.txt", "w");
    fprintf(rand_file, "%d\n", rand_number); 
    fclose(rand_file); 
    return 1; 
}
