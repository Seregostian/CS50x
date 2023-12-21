#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[]) {
  if (argc != 2) {
    printf("Usage: ./recover IMAGE\n");
    return 1;
  }

  FILE *file = fopen(argv[1], "r");
  if (file == NULL) {
    printf("Could not open file %s.\n", argv[1]);
    return 2;
  }

  BYTE buffer[512];
  char filename[8];

  int imageCount = 0;

  FILE *img = NULL;

  while (fread(buffer, sizeof(BYTE), 512, file) == 512) {
    if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
        (buffer[3] & 0xf0) == 0xe0) {
      if (img != NULL) {
        fclose(img);
      }

      sprintf(filename, "%03i.jpg", imageCount);
      img = fopen(filename, "w");
      if (img == NULL) {
        printf("Could not open file %s.\n", filename);
        return 3;
      }

      fwrite(&buffer, sizeof(BYTE), 512, img);
      imageCount++;
    } else if (imageCount > 0) {
      fwrite(&buffer, sizeof(BYTE), 512, img);
    }
  }

  fclose(file);
  fclose(img);

  return 0;
}
