#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>

#define MAX_CITIES 100
#define MAX_NAME_LEN 10

typedef struct {
    int num_cities;
    int cost_limit;
    char city_names[MAX_CITIES][MAX_NAME_LEN];
    int cost_matrix[MAX_CITIES][MAX_CITIES];
} Problem;

typedef struct {
    int pairs[MAX_CITIES/2][2]; // each pair stores city indices
    int cost;
} Solution;

// read problem data from file
Problem read_problem(const char* filename) {
    FILE* file = fopen(filename, "r");
    Problem problem;

    if (!file) {
        fprintf(stderr, "Error: Could not open file %s\n", filename);
        exit(1);
    }

    // read number of cities and cost limit
    fscanf(file, "%d %d", &problem.num_cities, &problem.cost_limit);

    // read city names
    for (int i = 0; i < problem.num_cities; i++) {
        fscanf(file, "%s", problem.city_names[i]);
    }

    // read the cost matrix
    for (int i = 0; i < problem.num_cities; i++) {
        for (int j = 0; j < problem.num_cities; j++) {
            char cost_str[MAX_NAME_LEN];
            fscanf(file, "%s", cost_str);

            if (strcmp(cost_str, "-") == 0) {
                problem.cost_matrix[i][j] = 0; // diagonal is zero cost
            } else {
                problem.cost_matrix[i][j] = atoi(cost_str);
            }
        }
    }

    fclose(file);
    return problem;
}

// format solution in lexicographical order
void format_solution(const Solution* solution, const Problem* problem, char* output) {
    char pairs[MAX_CITIES/2][MAX_NAME_LEN*2+1];

    // create strings for each city pair
    for (int i = 0; i < problem->num_cities/2; i++) {
        int city1 = solution->pairs[i][0];
        int city2 = solution->pairs[i][1];

        // order cities alphabetically within each pair
        if (strcmp(problem->city_names[city1], problem->city_names[city2]) <= 0) {
            sprintf(pairs[i], "%s%s", problem->city_names[city1], problem->city_names[city2]);
        } else {
            sprintf(pairs[i], "%s%s", problem->city_names[city2], problem->city_names[city1]);
        }
    }

    // sort pairs lexicographically
    for (int i = 0; i < problem->num_cities/2 - 1; i++) {
        for (int j = 0; j < problem->num_cities/2 - i - 1; j++) {
            if (strcmp(pairs[j], pairs[j+1]) > 0) {
                char temp[MAX_NAME_LEN*2+1];
                strcpy(temp, pairs[j]);
                strcpy(pairs[j], pairs[j+1]);
                strcpy(pairs[j+1], temp);
            }
        }
    }

    // combine pairs into output string
    output[0] = '\0';
    for (int i = 0; i < problem->num_cities/2; i++) {
        char pair_str[MAX_NAME_LEN*2+2];
        sprintf(pair_str, "%c%c%s", pairs[i][0], pairs[i][1], (i < problem->num_cities/2 - 1) ? " " : "");
        strcat(output, pair_str);
    }
}

// print solution to stdout
void print_solution(const Solution* solution, const Problem* problem) {
    char formatted[MAX_CITIES * MAX_NAME_LEN];
    format_solution(solution, problem, formatted);
    printf("%s\n", formatted);
}

// check if two solutions are identical
bool solutions_equal(const char* sol1, const char* sol2) {
    return strcmp(sol1, sol2) == 0;
}

// create a copy of a solution
Solution copy_solution(const Solution* src, int num_pairs) {
    Solution dst;
    dst.cost = src->cost;
    for (int i = 0; i < num_pairs; i++) {
        dst.pairs[i][0] = src->pairs[i][0];
        dst.pairs[i][1] = src->pairs[i][1];
    }
    return dst;
}

// find all partitions that meet the cost constraint
void find_partitions(const Problem* problem, bool optimize_only) {
    int num_cities = problem->num_cities;
    int num_pairs = num_cities / 2;
    int cost_limit = problem->cost_limit;

    // store found solutions to avoid duplicates
    char** solutions = NULL;
    int num_solutions = 0;

    // current solution being built
    Solution current;
    current.cost = 0;

    // best solution found so far
    Solution best;
    best.cost = INT_MAX;

    // track which cities we've used
    bool used[MAX_CITIES] = {false};

    // backtracking function
    void backtrack(int pair_idx) {
        // if all pairs are assigned, we have a solution
        if (pair_idx == num_pairs) {
            if (current.cost <= cost_limit) {
                char formatted[MAX_CITIES * MAX_NAME_LEN];
                format_solution(&current, problem, formatted);

                if (optimize_only) {
                    // update best solution if better
                    if (current.cost < best.cost) {
                        best = copy_solution(&current, num_pairs);
                    }
                } else {
                    // check for duplicates
                    bool duplicate = false;
                    for (int i = 0; i < num_solutions; i++) {
                        if (solutions_equal(formatted, solutions[i])) {
                            duplicate = true;
                            break;
                        }
                    }

                    if (!duplicate) {
                        // add to solutions list
                        solutions = realloc(solutions, (num_solutions + 1) * sizeof(char*));
                        solutions[num_solutions] = strdup(formatted);
                        num_solutions++;

                        // output solution
                        printf("%s\n", formatted);
                    }
                }
            }
            return;
        }

        // find first unused city
        int first = -1;
        for (int i = 0; i < num_cities; i++) {
            if (!used[i]) {
                first = i;
                break;
            }
        }

        if (first == -1) return; // should never happen

        // mark first city as used
        used[first] = true;

        // try pairing with other unused cities
        for (int second = 0; second < num_cities; second++) {
            if (!used[second]) {
                int pair_cost = problem->cost_matrix[first][second];

                // branch and bound - skip if too expensive
                if (current.cost + pair_cost > cost_limit) {
                    continue;
                }

                // add pair to solution
                current.pairs[pair_idx][0] = first;
                current.pairs[pair_idx][1] = second;
                current.cost += pair_cost;
                used[second] = true;

                // continue with next pair
                backtrack(pair_idx + 1);

                // backtrack
                used[second] = false;
                current.cost -= pair_cost;
            }
        }

        // backtrack first city
        used[first] = false;
    }

    // start the backtracking
    backtrack(0);

    // print optimal cost if in optimization mode
    if (optimize_only && best.cost != INT_MAX) {
        printf("%d\n", best.cost);
    }

    // free memory
    for (int i = 0; i < num_solutions; i++) {
        free(solutions[i]);
    }
    free(solutions);
}

int main(int argc, char* argv[]) {
    bool optimize_only = false;
    char* filename = NULL;

    // parse command line arguments
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-o") == 0) {
            optimize_only = true;
        } else {
            filename = argv[i];
        }
    }

    if (!filename) {
        fprintf(stderr, "Usage: %s [-o] <input_file>\n", argv[0]);
        return 1;
    }

    // read the problem and solve it
    Problem problem = read_problem(filename);
    find_partitions(&problem, optimize_only);

    return 0;
}
