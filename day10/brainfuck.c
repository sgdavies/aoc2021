#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_PROG_SIZE 20000
#define TAPE_LEN 1000
#define STACK_SIZE 100

int main(int argc, char** argv) {
	// Program
	char prog[MAX_PROG_SIZE] = {0};
	FILE *fp = fopen(argv[1], "r");
	if (fp == NULL) {
		printf("Failed to open program file %s\n", argv[1]);
		return -1;
	}
	int i=0;
	while (!feof(fp)) {
		prog[i++] = fgetc(fp);
	}
	prog[i] = '\0';
	fclose(fp);
	printf("Program length: %ld\n", strlen(prog));

	// Data
	char empty = '\0';
	char *data;
	long data_len = 0;
	if (argc > 2) {
	    fp = fopen(argv[2], "rb");  // Open the file in binary mode
            fseek(fp, 0, SEEK_END);          // Jump to the end of the file
            data_len = ftell(fp);             // Get the current byte offset in the file
            rewind(fp);                      // Jump back to the beginning of the file

            data = (char *)malloc(data_len * sizeof(char)); // Enough memory for the file
            fread(data, data_len, 1, fp); // Read in the entire file
            fclose(fp); // Close the file
	} else {
	    data = &empty;
	}
	printf("Data length: %ld\n", data_len);
	
	// Run the program
	long tape[TAPE_LEN] = {0};
	int dp = 0;
	int ip = 0;
	int sp = 0;
	int stack[STACK_SIZE] = {0};
	int depth, jmp;

	char cmd = prog[ip];
	while (cmd != '\0') {
//printf("%c", cmd);
		switch (cmd) {
			case '<':
				dp--;//printf("dp-- %d\n",dp);
				break;
			case '>':
				dp++;//printf("dp++ %d\n",dp);
				break;
			case '+':
				tape[dp]++;//printf("+ %d: %d\n",dp,tape[dp]);
				break;
			case '-':
				tape[dp]--;//printf("- %d: %d\n",dp,tape[dp]);
				break;
			case '.':
				printf("%ld ", tape[dp]);
				break;
			case ',':
				tape[dp] = *data++;
				break;
			case '[':
				if (tape[dp] == 0) { // Skip to matching ]
					depth = 1;
					while (depth > 0) {
						ip++;
						if (prog[ip] == '[') {
							depth++;
						} else if (prog[ip] == ']') {
							depth--;
						}
					}
				} else {
					// Save location to jump back to later
					//printf("\nstore stack sp %d ip %d\n",sp,ip);
					stack[sp++] = ip;
				}
				break;

			case ']':
				jmp = stack[--sp];
				//printf("\njmp %d t %d i %d\n", jmp,tape[dp],ip);
				if (tape[dp] != 0) {
					ip = jmp -1;
				}
				break;

			default:
				// Ignore all other characters
				break;
		}

		cmd = prog[++ip];
	}

	printf("\n");
	return 0;
}
