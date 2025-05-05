#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>

#define MAX_SIZE 100
#define MAX_LINE_LENGTH 1024

// holds weights for all edges
typedef struct {
    double down[MAX_SIZE][MAX_SIZE];   // north-south streets (vertical)
    double right[MAX_SIZE][MAX_SIZE];  // west-east streets (horizontal)
    double diag[MAX_SIZE][MAX_SIZE];   // diagonal streets (if applicable)
    int rows;                          // number of rows in the grid
    int cols;                          // number of columns in the grid
} Grid;

// represents a move in the grid
typedef enum {
    EAST = 'E',
    SOUTH = 'S',
    DIAGONAL = 'D'
} Direction;

// function declarations
void parse_file(const char *filename, Grid *grid, bool diagonal_mode);
void solve_manhattan_tourist(Grid *grid, bool diagonal_mode, bool traceback_mode);
void skip_comments_and_whitespace(FILE *file, char *line, size_t max_length);
void print_path(char *path, int path_length);

int main(int argc, char *argv[]) {
    bool diagonal_mode = false;
    bool traceback_mode = false;
    char *filename = NULL;

    // parse command line arguments
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-d") == 0) {
            diagonal_mode = true;
        } else if (strcmp(argv[i], "-t") == 0) {
            traceback_mode = true;
        } else {
            filename = argv[i];
        }
    }

    if (filename == NULL) {
        fprintf(stderr, "Usage: %s [-d] [-t] input_file\n", argv[0]);
        return 1;
    }

    Grid grid;
    parse_file(filename, &grid, diagonal_mode);
    solve_manhattan_tourist(&grid, diagonal_mode, traceback_mode);

    return 0;
}

// skip comments (lines starting with #) and empty lines
void skip_comments_and_whitespace(FILE *file, char *line, size_t max_length) {
    while (fgets(line, max_length, file) != NULL) {
        // remove comments (everything after and including #)
        char *comment_start = strchr(line, '#');
        if (comment_start != NULL) {
            *comment_start = '\0';
        }

        // check if the line has any non-whitespace characters
        bool has_content = false;
        for (int i = 0; line[i] != '\0'; i++) {
            if (!isspace(line[i])) {
                has_content = true;
                break;
            }
        }

        if (has_content) {
            break;  // found a non-empty line
        }
    }
}

// parse the input file and store the grid weights
void parse_file(const char *filename, Grid *grid, bool diagonal_mode) {
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        perror("Error opening file");
        exit(1);
    }

    char line[MAX_LINE_LENGTH];

    // initialize grid with all zero weights
    memset(grid, 0, sizeof(Grid));

    if (diagonal_mode) {
        // for HVD format, we need to parse sections marked by #G_down, #G_right, and #G_diag
        enum { NONE, DOWN, RIGHT, DIAG } section = NONE;
        int down_row = 0, right_row = 0, diag_row = 0;

        while (fgets(line, sizeof(line), file)) {
            // check for section headers
            if (strstr(line, "#G_down:")) {
                section = DOWN;
                // extract dimensions
                sscanf(line, "#G_down: %d %d", &grid->rows, &grid->cols);
                continue;
            } else if (strstr(line, "#G_right:")) {
                section = RIGHT;
                continue;
            } else if (strstr(line, "#G_diag:")) {
                section = DIAG;
                continue;
            } else if (strstr(line, "#---")) {
                section = NONE;
                continue;
            }

            // skip comments and empty lines
            char *comment_start = strchr(line, '#');
            if (comment_start != NULL) {
                *comment_start = '\0';
            }

            // check if line is empty after removing comments
            bool has_content = false;
            for (int i = 0; line[i] != '\0'; i++) {
                if (!isspace(line[i])) {
                    has_content = true;
                    break;
                }
            }

            if (!has_content) {
                continue;
            }

            // process the line based on current section
            char *token = strtok(line, " \t\n");
            int col = 0;

            switch (section) {
                case DOWN:
                    if (down_row < grid->rows) {
                        while (token != NULL && col < grid->cols) {
                            grid->down[down_row][col] = atof(token);
                            token = strtok(NULL, " \t\n");
                            col++;
                        }
                        down_row++;
                    }
                    break;

                case RIGHT:
                    if (right_row < grid->rows + 1) {
                        while (token != NULL && col < grid->cols) {
                            grid->right[right_row][col] = atof(token);
                            token = strtok(NULL, " \t\n");
                            col++;
                        }
                        right_row++;
                    }
                    break;

                case DIAG:
                    if (diag_row < grid->rows) {
                        while (token != NULL && col < grid->cols) {
                            grid->diag[diag_row][col] = atof(token);
                            token = strtok(NULL, " \t\n");
                            col++;
                        }
                        diag_row++;
                    }
                    break;

                default:
                    break;
            }
        }

        if (grid->rows == 0 || grid->cols == 0) {
            fprintf(stderr, "Invalid input file format\n");
            exit(1);
        }
    } else {
        // for simple HV format - detect grid dimensions from the input

        // Count the number of lines to determine rows and cols
        int total_lines = 0;
        int max_cols = 0;

        // First pass to determine dimensions
        while (fgets(line, sizeof(line), file)) {
            // Skip comments
            char *comment_start = strchr(line, '#');
            if (comment_start != NULL) {
                *comment_start = '\0';
            }

            // Check if line is empty after removing comments
            bool has_content = false;
            for (int i = 0; line[i] != '\0'; i++) {
                if (!isspace(line[i])) {
                    has_content = true;
                    break;
                }
            }

            if (!has_content) {
                continue;
            }

            // Count columns in this line
            int cols = 0;
            char *token = strtok(line, " \t\n");
            while (token != NULL) {
                cols++;
                token = strtok(NULL, " \t\n");
            }

            if (cols > max_cols) {
                max_cols = cols;
            }

            total_lines++;
        }

        // Reset file pointer to beginning
        rewind(file);

        // Calculate rows and cols based on total lines
        // For an n×m grid, we have n rows of down weights and n+1 rows of right weights
        // Total lines = n + (n+1) = 2n+1
        grid->rows = (total_lines - 1) / 2;
        grid->cols = max_cols;

        // Now read the weights
        int curr_line = 0;

        // Read all content lines
        while (fgets(line, sizeof(line), file)) {
            // Skip comments
            char *comment_start = strchr(line, '#');
            if (comment_start != NULL) {
                *comment_start = '\0';
            }

            // Check if line is empty after removing comments
            bool has_content = false;
            for (int i = 0; line[i] != '\0'; i++) {
                if (!isspace(line[i])) {
                    has_content = true;
                    break;
                }
            }

            if (!has_content) {
                continue;
            }

            char *temp_line = strdup(line);  // Make a copy for processing
            if (temp_line == NULL) {
                perror("Memory allocation failed");
                exit(1);
            }

            // Process line based on the current line number
            if (curr_line < grid->rows) {
                // This is a down weight line
                char *token = strtok(temp_line, " \t\n");
                int j = 0;

                while (token != NULL && j < grid->cols) {
                    grid->down[curr_line][j] = atof(token);
                    token = strtok(NULL, " \t\n");
                    j++;
                }
            } else {
                // This is a right weight line
                int right_row = curr_line - grid->rows;

                char *token = strtok(temp_line, " \t\n");
                int j = 0;

                while (token != NULL && j < grid->cols) {
                    grid->right[right_row][j] = atof(token);
                    token = strtok(NULL, " \t\n");
                    j++;
                }
            }

            free(temp_line);
            curr_line++;
        }
    }

    fclose(file);
}

// solve the manhattan tourist problem using dynamic programming
void solve_manhattan_tourist(Grid *grid, bool diagonal_mode, bool traceback_mode) {
    int rows = grid->rows;
    int cols = grid->cols;

    // dp table to store maximum weight at each position
    double dp[MAX_SIZE + 1][MAX_SIZE + 1];

    // traceback matrix to store the direction we came from
    Direction traceback[MAX_SIZE + 1][MAX_SIZE + 1];

    // initialize first cell (top-left corner)
    dp[0][0] = 0.0;

    // fill the first column (can only go south)
    for (int i = 1; i <= rows; i++) {
        dp[i][0] = dp[i-1][0] + grid->down[i-1][0];
        traceback[i][0] = SOUTH;
    }

    // fill the first row (can only go east)
    for (int j = 1; j <= cols; j++) {
        dp[0][j] = dp[0][j-1] + grid->right[0][j-1];
        traceback[0][j] = EAST;
    }

    // fill the rest of the dp table
    for (int i = 1; i <= rows; i++) {
        for (int j = 1; j <= cols; j++) {
            // Initialize with move from the top (south move)
            double from_top = dp[i-1][j] + grid->down[i-1][j];
            double from_left = dp[i][j-1] + grid->right[i][j-1];
            double from_diag = -1.0;  // initialize to negative to indicate not set

            // Set default value with south preference
            if (from_top >= from_left) {
                dp[i][j] = from_top;
                traceback[i][j] = SOUTH;
            } else {
                dp[i][j] = from_left;
                traceback[i][j] = EAST;
            }

            // if diagonal mode is enabled, consider diagonal move
            if (diagonal_mode && i > 0 && j > 0) {
                from_diag = dp[i-1][j-1] + grid->diag[i-1][j-1];

                if (from_diag > dp[i][j]) {
                    dp[i][j] = from_diag;
                    traceback[i][j] = DIAGONAL;
                }
            }
        }
    }

    // print the maximum weight
    printf("%.0f\n", dp[rows][cols]);

    // if traceback mode is enabled, print the path
    if (traceback_mode) {
        // reconstruct the path
        char path[2 * MAX_SIZE]; // maximum path length is rows + cols steps
        int path_length = 0;

        // start from the bottom right
        int i = rows;
        int j = cols;

        while (i > 0 || j > 0) {
            Direction dir = traceback[i][j];
            path[path_length++] = dir;

            // move according to the traceback direction
            if (dir == EAST) {
                j--;
            } else if (dir == SOUTH) {
                i--;
            } else if (dir == DIAGONAL) {
                i--;
                j--;
            }
        }

        // reverse the path (since we traced from end to start)
        for (int i = 0; i < path_length / 2; i++) {
            char temp = path[i];
            path[i] = path[path_length - 1 - i];
            path[path_length - 1 - i] = temp;
        }

        // print the path
        print_path(path, path_length);
    }
}

// print the path in the specified format (ESEDES...)
void print_path(char *path, int path_length) {
    for (int i = 0; i < path_length; i++) {
        printf("%c", path[i]);
    }
    printf("\n");
}