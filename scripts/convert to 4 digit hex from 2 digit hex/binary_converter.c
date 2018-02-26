#include <string.h>
#include <stdio.h>
#include <stdint.h>

/**
  * Reads data from the first argument file and prints it to output.bin as binary data.
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

  char* x[2];
  char* y[2];

  //Read 2 lines (2 value) and output a 4 digit hex.
  while (fscanf(file_r, "%s", x) != EOF && fscanf(file_r, "%s", y) != EOF) {
    fwrite ((const void*) x, 2, 1, file_w); 
    fwrite ((const void*) y, 2, 1, file_w); 
    fwrite ("\n", 1, 1, file_w); 

  }

  fclose (file_r);
  fclose (file_w);
  return 1;
}

