#include <string.h>
#include <stdio.h>
#include <stdint.h>

/**
  * Reads data from the first argument file and prints it to output.bin as binary data.
  */
int
main(int argc, char *argv[])
{
  printf("Starting to analyse data from file 'data.txt'. Converting to output file 'output.bin'.\n");

  FILE* file_r;
  FILE* file_w;

  //file_r = fopen(argv[1], "r");
  file_r = fopen("data.txt", "r");
  if (file_r == NULL) {
    printf("Could not open file_r.\n");
    return -1;
  }

  file_w = fopen("output.bin", "wb");

  if (file_w == NULL) {
    printf("Could not open output file\n");
    return -1;
  }

  uint16_t x;

  //Read a hexadecimal value and a space.
  while (fscanf(file_r, "%hu", &x) != EOF) {
    fwrite ((const void*) &x, 2, 1, file_w); 
  }

  fclose (file_r);
  fclose (file_w);
  return 1;
}

