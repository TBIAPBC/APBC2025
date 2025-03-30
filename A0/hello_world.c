#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
 	// point to input file and outputfile as given by command line arguments
	char *input_filename = argv[1];
	
	// open the input file for reading
	FILE *input_file = fopen(input_filename, "r");
	
	// set up buffer for input file content (files are written sequentially)
	// step 1: determine input file size
	fseek(input_file, 0, SEEK_END);
	long file_size = ftell(input_file);
	fseek(input_file, 0, SEEK_SET);
	// step 2: dynamically allocate buffer memory corresponding to input file size
	char *content = (char *)malloc(file_size + 1);
	
	// read input file content to buffer
	fread(content, sizeof(char), file_size, input_file);


	// print text to standard output
	printf("Hello, World!\n%s", content);
	
	// free buffer memory
	free(content);

	return 0;
}	
