
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <math.h>


int main(int argc, char const *argv[])
{
  FILE* in = fopen("numbers.txt", "r");
  if (!in) {
    return 1;
  }
  FILE* out = fopen("numbers.bin", "w");
  if (!out) {
    return 2;
  }

  uint16_t v;
  while(fscanf(in, "%hu ", &v) != EOF) {
    fwrite(&v, 2, 1, out);
  }

  fclose(out);
  return 0;
}