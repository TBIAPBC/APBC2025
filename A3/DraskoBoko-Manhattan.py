# This script was generated with the help of AI tool ChatGPT

import sys
import argparse

def read_input_lines(lines, diagonal_flag):
    lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith('#')]
    rows = [list(map(float, line.split())) for line in lines]

    m = max(len(row) for row in rows)
    m_rows = [row for row in rows if len(row) == m]
    n_minus_1 = len(m_rows)
    n = n_minus_1 + 1

    G_down = rows[:n_minus_1]
    G_right = rows[n_minus_1:n_minus_1 + n]
    
    # Include diagonal weights only if -d flag is provided
    if diagonal_flag:
        G_diag = rows[n_minus_1 + n:]
    else:
        G_diag = None

    return n, m, G_down, G_right, G_diag

def manhattan_tourist(n, m, G_down, G_right, G_diag=None):
    s = [[0] * m for _ in range(n)]
    backtrack = [[None] * m for _ in range(n)]

    for i in range(1, n):
        s[i][0] = s[i-1][0] + G_down[i-1][0]
        backtrack[i][0] = 'S'
    for j in range(1, m):
        s[0][j] = s[0][j-1] + G_right[0][j-1]
        backtrack[0][j] = 'E'

    for i in range(1, n):
        for j in range(1, m):
            down = s[i-1][j] + G_down[i-1][j]
            right = s[i][j-1] + G_right[i][j-1]
            diagonal = float('-inf')
            if G_diag:
                diagonal = s[i-1][j-1] + G_diag[i-1][j-1]
            max_val = max(down, right, diagonal)

            s[i][j] = max_val
            if max_val == down:
                backtrack[i][j] = 'S'
            elif max_val == diagonal:
                backtrack[i][j] = 'D'
            else:
                backtrack[i][j] = 'E'

    return s, backtrack

def traceback(n, m, backtrack):
    i, j = n - 1, m - 1
    path = []
    while i > 0 or j > 0:
        move = backtrack[i][j]
        path.append(move)
        if move == 'S':
            i -= 1
        elif move == 'E':
            j -= 1
        elif move == 'D':
            i -= 1
            j -= 1
    return ''.join(reversed(path))

def main():
    parser = argparse.ArgumentParser(description="Compute max score and best path for the Manhattan Tourist Problem.")
    parser.add_argument("input", help="Input file path")
    parser.add_argument("-d", action="store_true", help="Enable processing diagonal edge weights")
    parser.add_argument("-t", action="store_true", help="Print the best path")

    args = parser.parse_args()

    with open(args.input) as f:
        lines = f.readlines()

    n, m, G_down, G_right, G_diag = read_input_lines(lines, args.d)
    s, backtrack = manhattan_tourist(n, m, G_down, G_right, G_diag)

    # Print the score at the bottom-right of the matrix (max score)
    print(int(s[n-1][m-1]) if s[n-1][m-1].is_integer() else s[n-1][m-1])

    # If -t flag is set, print the best path
    if args.t:
        path = traceback(n, m, backtrack)
        print(path)

if __name__ == "__main__":
    main()
