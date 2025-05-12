import sys
import copy



# - - - - - - - READ COMMANDLINE ARGUMENTS - - - - - - - 

traceback_mode = False
diagonal_mode = False

try:
    inputfilename = sys.argv[1]
    try:
        for i in range(2, 4, 1):
            if sys.argv[i] == "-t":
                traceback_mode = True
            elif sys.argv[i] == "-d":
                diagonal_mode = True
    except IndexError:
        pass
except IndexError:
    print("\n\n\n\nERROR. Usage: python programmname.py <inputfile> [-t] [-d]\n\n\n")





# - - - - - - - READ_INPUTFILE  - - - - - - -     

with open (inputfilename, "r") as inputfile:
    
    all_weights = []                                # creates a list of lists, containing all weights as float
   
    for line in inputfile:
        line = line.strip()
        if not line.startswith("#"):                # ignore all lines that start with #
            if line:
                row = []
                for weight in line.split():
                    row.append(float(weight))
                all_weights.append(row) 
    
    #print("all: ", all_weights, "\n\n")

    #EXTRACT DOWN_WEIGHTS MATRIX OUT OF ALL_WEIGHTS
    down_weights = []
    number_of_down_weights_per_row = len(all_weights[0])                                    
    number_of_down_weights_rows = 0
    for i in range(len(all_weights)):       
        if len(all_weights[i]) == number_of_down_weights_per_row:
            number_of_down_weights_rows += 1
    
    for i in range(0, number_of_down_weights_rows):
        row = []
        for j in range(0, number_of_down_weights_per_row):
            weight = all_weights[i][j]
            row.append(weight)
        down_weights.append(row)

    #print("Down ", down_weights, "\n\n")


    #EXTRACT RIGHT_WEIGHTS MATRIX OUT OF ALL_WEIGHTS    
    right_weights = []
    number_of_right_weights_per_row = number_of_down_weights_per_row - 1
    number_of_right_weights_rows = number_of_down_weights_rows + 1  

    for i in range(number_of_down_weights_rows, number_of_down_weights_rows+number_of_right_weights_rows):
        row = []
        for j in range(0, number_of_right_weights_per_row):    
            weight = all_weights[i][j]
            row.append(weight)
        right_weights.append(row)

    #print("right: ", right_weights, "\n\n")


    #EXTRACT DIAGONAL_WEIGHTS MATRIX OUT OF ALL_WEIGHTS
    if diagonal_mode == True:
        try:
            diagonal_weights = []
            number_of_diagonal_weights_per_row =  number_of_down_weights_per_row - 1
            number_of_diagonal_weights_rows = number_of_down_weights_rows
            
            for i in range(number_of_right_weights_rows + number_of_down_weights_rows, number_of_down_weights_rows + number_of_diagonal_weights_rows + number_of_right_weights_rows):
                row = []
                for j in range(0, number_of_diagonal_weights_per_row):          
                    weight = all_weights[i][j]
                    row.append(weight)
                diagonal_weights.append(row)
            
        except IndexError:
            print("\nERROR: You used -d as argument but have no diagonal edges in your input file.\n")
            pass

        #print("Dia: ", diagonal_weights, "\n\n")



# - - - - - - - SCORE_MATRIX - - - - - - - 

N_number_of_rows = 0
M_number_of_columns = 0

for row in right_weights:
    N_number_of_rows += 1
for value in down_weights[0]:
    M_number_of_columns += 1

scores = []                                                                 # initialize score matrix
initial_value = 0.0 
     
for _ in range(N_number_of_rows):                                           # sets all values in score matrix to 0
    row = []
    for _ in range(M_number_of_columns):
        row.append(initial_value)
    scores.append(row)


for j in range(1, M_number_of_columns):                                     # first row
    scores[0][j] = scores[0][j-1] + right_weights[0][j-1]
    
for i in range(1, N_number_of_rows):                                        # first column
    scores[i][0] = scores[i-1][0] + down_weights[i-1][0]

for i in range(1, N_number_of_rows):                                        # rest of matrix
    for j in range(1, M_number_of_columns):
        if diagonal_mode == False:
            scores[i][j] = max(scores[i][j-1] + right_weights[i][j-1], 
                                scores[i-1][j] + down_weights[i-1][j])
        elif diagonal_mode == True:
            try:
                scores[i][j] = max(scores[i][j-1] + right_weights[i][j-1], 
                                    scores[i-1][j] + down_weights[i-1][j],
                                    scores[i-1][j-1] + diagonal_weights[i-1][j-1])
            except:
                pass




# - - - - - - - TRACEBACK - - - - - - - 

if traceback_mode == True:
    reversed_path = []
    i = N_number_of_rows - 1                            # [i][j] now equals the "coordinates" of the sink-node (finish-node)
    j = M_number_of_columns - 1

    while i > 0 or j > 0:
        current_node_score = scores[i][j]

        # check if we came from North
        if current_node_score == scores[i-1][j] + down_weights[i-1][j]:
            reversed_path.append("S")
            i -= 1
        
        # check if we came from West
        elif current_node_score == scores[i][j-1] + right_weights[i][j-1]:
            reversed_path.append("E")
            j -= 1

        # check if we came from Northwest 
        try:
            if diagonal_mode == True and i > 0 and j > 0 and current_node_score == scores[i-1][j-1] + diagonal_weights[i-1][j-1]:
                reversed_path.append("D")
                i -= 1
                j -= 1
        except: 
            break
        
    # reverse it because we calculated the path from sink to source
    path = list(reversed(reversed_path))




# - - - - - - - PRINT RESULTS - - - - - - - 

optimal_score = scores[N_number_of_rows-1][M_number_of_columns-1]
print(optimal_score)
if traceback_mode == True:
    for i in range(len(path)):
        print(path[i], end="")



