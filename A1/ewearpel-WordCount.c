#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <locale.h>

// define the expected maximum word length (longest word in English dictionaries is 45 letters
// so just to be safe I chose 50; define max. number of unique words to store
#define MAX_WORD_LENGTH 50
#define MAX_WORDS 10000

// define structure to capture words and their counts
typedef struct {
  char word[MAX_WORD_LENGTH];
  int count;
} WordCount;

// set up array to store words and frequencies
WordCount word_list[MAX_WORDS];
int word_count = 0; // Counter for number of unique words

// define function prototypes
void count_words(FILE *filepath, int ignore_case, int print_list);
int compare(const void *a, const void *b);
char* handle_case(char *word, int ignore_case);
WordCount* find_word(char *word);

int main(int argc, char *argv[]) {
  // recognize umlaute
  setlocale(LC_ALL, "");

  int ignore_case = 0;
  int print_list = 0;
  FILE *file = stdin;  // Default to stdin if no file is provided
  int file_provided = 0;

  // parse command line arguments
  for (int i = 1; i < argc; i++) {
    if (strcmp(argv[i], "-I") == 0) {
      ignore_case = 1;
    } else if (strcmp(argv[i], "-l") == 0) {
      print_list = 1;
    } else {
      // If a file is provided, open it
      file = fopen(argv[i], "r");
      if (!file) {
        fprintf(stderr, "Error opening file: %s\n", argv[i]);
        return 1;
      }
      file_provided = 1;
    }
  }

  // count the words
  count_words(file, ignore_case, print_list);

  // close the file if it's not stdin
  if (file_provided) {
    fclose(file);
  }

  return 0;
}

// function to determine if a character should be considered part of a word;
// this includes regular alphanumeric chars and extended chars (like umlauts)
int is_word_char(unsigned char c) {
  if (isalnum((unsigned char)c)) return 1;

  // accept umlauts and other extended characters;
  // this range includes most Latin extended characters
  if (c >= 128) return 1;

  return 0;
}

// define the functions to be used
void count_words(FILE *filepath, int ignore_case, int print_list) {
  // set up buffer for every word
  char buffer[MAX_WORD_LENGTH];

  // read each word from input file;
  // fscanf reads formatted file, %s specifies string format, returns 1 if word is successfully read
  while (fscanf(filepath, "%s", buffer) == 1) {
    // handle case of word in the buffer
    char *unicase_word = handle_case(buffer, ignore_case);

    // if there's a word in the buffer
    if (strlen(unicase_word) > 0) {
      // check if word has been found before
      WordCount* word = find_word(unicase_word);

      if (word) {
        word->count++;
      } else {
        // if word not yet found, add it to list
        if (word_count < MAX_WORDS) {
          strcpy(word_list[word_count].word, unicase_word);
          word_list[word_count].count = 1;
          word_count++;
        }
      }
    }
  }

  // print the unique/total word count
  if (!print_list) {
    int total_word_count = 0;
    for (int i = 0; i < word_count; i++) {
      total_word_count += word_list[i].count;
    }
    printf("%d / %d\n", word_count, total_word_count);
  }


  // now print_list if flag is used
  if (print_list) {
    // sort by frequency; for equal frequency by alphabet
    qsort(word_list, word_count, sizeof(WordCount), compare);
    for (int i = 0; i < word_count; i++) {
      printf("%s %d\n", word_list[i].word, word_list[i].count);
    }
  }
}

int compare(const void *a, const void *b) {
  WordCount* word_a = (WordCount*) a;
  WordCount* word_b = (WordCount*) b;

  // compare by frequency and alphabetically if frequencies are equal
  if (word_a->count > word_b->count) {
    return -1; // Reverse order for descending frequency
  } else if (word_a->count < word_b->count) {
    return 1;
  }

  return strcmp(word_a->word, word_b->word); // sort alphabetically if frequencies are the same
}

char* handle_case(char *word, int ignore_case) {
  // static array to hold the cleaned word
  static char cleaned[MAX_WORD_LENGTH];
  int j = 0;

  // loop through every character of the 'word'
  for (int i = 0; word[i] != '\0'; i++) {
    // check if the character is part of a word
    if (is_word_char((unsigned char)word[i])) {
      // if ignore_case is 1, convert the character to lowercase, else keep it as it is
      cleaned[j++] = ignore_case ? tolower((unsigned char)word[i]) : word[i];
    }
  }

  // after processing all characters, add a null terminator to the cleaned word
  cleaned[j] = '\0';

  return cleaned;
}

WordCount* find_word(char *word) {
  for (int i = 0; i < word_count; i++) {
    if (strcmp(word_list[i].word, word) == 0) {
      return &word_list[i];
    }
  }
  return NULL;
}
