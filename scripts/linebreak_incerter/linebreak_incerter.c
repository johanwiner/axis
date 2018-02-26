#include <string.h>
#include <stdio.h>
#include <stdint.h>

/**
  * Reads data from data.txt file and prints it to output.txt with a line break after each number.
  */
int
main(int argc, char *argv[])
{
  printf("Starting to analyse data from file 'data.txt'. Converting to output file 'output.txt'.\n");

  FILE* file_r;
  FILE* file_w;

  //file_r = fopen(argv[1], "r");
  file_r = fopen("data.txt", "r");
  if (file_r == NULL) {
    printf("Could not open file_r.\n");
    return -1;
  }

  file_w = fopen("output.txt", "w");

  if (file_w == NULL) {
    printf("Could not open output file\n");
    return -1;
  }

  uint16_t x;
  uint16_t count = 0;
	uint16_t i = 0;
  //Read a hexadecimal value and a space.
  while (fscanf(file_r, "%hu ", &x) != EOF) {
	++i;
	++count;
     if (i == 10) 
     {
       fprintf(file_w, "%d,\n", x);
	i = 0;
     }
     else 
       fprintf(file_w, "%d, ", x);
  }

printf("Converted %d nbr of samples.\n", count);
  fclose (file_r);
  fclose (file_w);
  return 1;
}

