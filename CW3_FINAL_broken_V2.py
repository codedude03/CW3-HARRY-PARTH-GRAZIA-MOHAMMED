#!/usr/bin/env python3

import copy
import time
import sys
import os
import random
import matplotlib.pyplot as plt
import CW3_profile_grids as sgd
USAGE_MESSAGE = "Usage: ./CW3_INPUT_OUTPUT.py (-flag). Where -flag is of the\
 formats:\n -explain, -file INPUT_file OUTPUT_file, -hint N, -profile\n\
 or a combination of them all"
 # this tells us how to input the arguments
MAX_FLAG_CMMDS = 5
POSSIBLE_FLAGS = ['-explain', '-file', '-hint', '-profile', '-wavefront']
grid1 = [
    [1, 0, 4, 2],
    [4, 2, 1, 3],
    [2, 1, 3, 4],
    [3, 4, 2, 1]]


grid2 = [
    [1, 0, 4, 2],
    [4, 2, 1, 3],
    [2, 1, 0, 4],
    [3, 4, 2, 1]]

grid3 = [
    [1, 0, 4, 2],
    [4, 2, 1, 0],
    [2, 1, 0, 4],
    [0, 4, 2, 1]]

grid4 = [
    [1, 0, 4, 2],
    [0, 2, 1, 0],
    [2, 1, 0, 4],
    [0, 4, 2, 1]]

grid5 = [
    [1, 0, 0, 2],
    [0, 0, 1, 0],
    [0, 1, 0, 4],
    [0, 0, 0, 1]]

grid6 = [
    [0, 0, 6, 0, 0, 3],
    [5, 0, 0, 0, 0, 0],
    [0, 1, 3, 4, 0, 0],
    [0, 0, 0, 0, 0, 6],
    [0, 0, 1, 0, 0, 0],
    [0, 5, 0, 0, 6, 4]]

grid7 = [
    [6, 1, 9, 8, 4, 2, 5, 3, 7, ],
    [7, 0, 5, 3, 6, 9, 1, 8, 2, ],
    [8, 3, 2, 1, 7, 5, 0, 0, 9, ],
    [1, 5, 8, 6, 9, 7, 3, 2, 4, ],
    [0, 6, 4, 2, 0, 1, 8, 7, 5, ],
    [2, 0, 3, 0, 8, 4, 6, 9, 1, ],
    [4, 0, 7, 9, 5, 6, 2, 0, 3, ],
    [3, 9, 1, 4, 0, 0, 7, 5, 6, ],
    [5, 2, 0, 7, 1, 3, 9, 4, 8, ]]

grids = [(grid1, 2, 2), (grid2, 2, 2), (grid3, 2, 2), (grid4, 2, 2), (grid5, 2, 2), (grid6, 2, 3), (grid7, 3, 3)]

profile_grids = sgd.profile_grids_1

'''
===================================
DO NOT CHANGE CODE ABOVE THIS LINE
===================================
'''
def check_section(section, n):

        if len(set(section)) == len(section) and sum(section) == sum([i for i in range(n+1)]):
                return True
        return False


def get_squares(grid, n_rows, n_cols):

        squares = []
        for i in range(n_cols):
                rows = (i*n_rows, (i+1)*n_rows)
                for j in range(n_rows):
                        cols = (j*n_cols, (j+1)*n_cols)
                        square = []
                        for k in range(rows[0], rows[1]):
                                line = grid[k][cols[0]:cols[1]]
                                square +=line
                        squares.append(square)


        return(squares)


def check_solution(grid, n_rows, n_cols):
        '''
        This function is used to check whether a sudoku board has been correctly solved

        args: grid - representation of a suduko board as a nested list.
        returns: True (correct solution) or False (incorrect solution)
        '''
        n = n_rows*n_cols

        for row in grid:
                if check_section(row, n) == False:
                        return False

        for i in range(n_rows**2):
                column = []
                for row in grid:
                        column.append(row[i])
                if check_section(column, n) == False:
                        return False

        squares = get_squares(grid, n_rows, n_cols)
        for square in squares:
                if check_section(square, n) == False:
                        return False

        return True

class EmptyCells:
    og_empty_cells = []
    
    def __init__(self, x):
        self.x = x
        EmptyCells.og_empty_cells = self  # Set the instance as a class variable
    
    def __str__(self):
        return str(self.x)
    
class SolutionSteps:
    explain_points = []
    
    def __init__(self, x):
        self.x = x
        SolutionSteps.explain_points = self  # Set the instance as a class variable
    
    def __str__(self):
        return str(self.x)


def get_og_empty_cells(empty_cells):
    if not EmptyCells.og_empty_cells:
        EmptyCells.og_empty_cells = empty_cells
    
    return

def dup_check(grid_to_check, n_rows, n_cols, location, i, n):
        #function to check for duplicate in row column reduce redundant tests
        
        #check in row
        if i in grid_to_check[location[0]]:
                return False
        
        #create column list
        column_list = []
        for row in grid_to_check:
                column_list.append(row[location[1]])
        #check in column
        if i in column_list:
                return False

        #calculate which square index returned from get_squares() to consider,
        #by working out position of box that contains location and multiplying
        #number box rows above by number box columns to get index.
        num_vert = n/n_rows
        num_horz = n/n_cols
        square_num = int(int(location[0]/n_rows)*num_horz) + int(location[1]/n_cols)
        #get the squares and identify the square to check in
        squares = get_squares(grid_to_check, n_rows, n_cols)
        square = squares[square_num]
        #check in square
        if i in square:
                return False

        #return true if no duplicates found
        return True
    
original_empty_cells = []
# global spaces_filled
spaces_filled = 0
global hint_grids
hint_grids = []

def random_solve(grid, n_rows, n_cols, max_tries=900000000):

        '''
        This function uses random trial and error to solve a Sudoku grid
        args: grid, n_rows, n_cols, max_tries
        return: A solved grid (as a nested list), or the original grid if no solution is found
        '''
        
        def fill_board_randomly(grid, n_rows, n_cols):
                '''
                This function will fill an unsolved Sudoku grid with random numbers
                args: grid, n_rows, n_cols
                return: A grid with all empty values filled in
                '''
                n = n_rows*n_cols
                #Make a copy of the original grid
                filled_grid = copy.deepcopy(grid)

                #Loop through the rows
                for i in range(len(grid)):
                        #Loop through the columns
                        for j in range(len(grid[0])):
                                #If we find a zero, fill it in with a random integer
                                if grid[i][j] == 0:
                                        filled_grid[i][j] = random.randint(1, n)

                return filled_grid

        for i in range(max_tries):
                possible_solution = fill_board_randomly(grid, n_rows, n_cols)
                if check_solution(possible_solution, n_rows, n_cols):
                        return possible_solution

        return grid

def recursive_plus_solve(grid, n_rows, n_cols):
        global spaces_filled
        global hint_grid_outputted
    
        #N is the maximum integer considered in this board
        n = n_rows*n_cols

        #temp_grid used to test possibles
        temp_grid = copy.deepcopy(grid)

        #print(grid)

        #check if grid full, therefore check if solution found
        #if there are any 0s, the below would return True (not False), meaning there are still empty spaces
        if not any(0 in sublist for sublist in temp_grid):
                if check_solution(grid, n_rows, n_cols):
                        return temp_grid
                return False

        #locate empty cells and store in array of tuples
        empty_cells = []
        row = 0
        index_found = False
        #iterate though rows and columns, if the cell is 0 add location tuple to array
        for row in range(len(temp_grid)):
                for column, cell in enumerate(temp_grid[row]):
                        if cell == 0:
                                location = (row, column)
                                empty_cells.append(location)
        
##        global original_empty_cells
##        # original_empty_cells = empty_cells[:] 
##        if not original_empty_cells:
##            original_empty_cells = copy.deepcopy(empty_cells)

        get_og_empty_cells(empty_cells)
                                
        empty_cell_possibles = []
        #this section checks for what values can go in each empty cell based on duplicates in row/column/box
        for cell_num, location in enumerate(empty_cells): #iterate empty cells, use enumerate to get cell num
                list_pos = []
                for i in range(1,n+1):
                        #check for duplicates within column/row/box
                        if dup_check(temp_grid, n_rows, n_cols, location, i, n):
                                list_pos.append(i) #add possible value to list
                                
                #add list of possible values for cell to list of values for all empty cells
                empty_cell_possibles.append(list_pos)
        
        # print(empty_cell_possibles)
        #identify least possible values and location of the cell
        least_possible = min(empty_cell_possibles, key=len)
        location = empty_cells[empty_cell_possibles.index(least_possible)]
        location_readable = tuple(i+1 for i in location)

        #for the least value cell, iterate the possibles and recursive solve for each, returning the solution if found
        for possible_val in least_possible:
                temp_grid[location[0]][location[1]] = possible_val

                # Section which gives the users hints
                spaces_filled += 1
                hint_grids.append(temp_grid)
                if generate_hints:
                        if not hint_grid_outputted:
                                if NUMBER_OF_HINTS == spaces_filled:
                                        give_solution_hints(NUMBER_OF_HINTS, hint_grids[NUMBER_OF_HINTS - 1])
                                        hint_grid_outputted = True
                
                attempt = recursive_plus_solve(temp_grid, n_rows, n_cols)
                # print(attempt)
                if attempt:
                        
                        #explanation_points.append(f"\nPut {possible_val} in location {location_readable}.")
                        SolutionSteps.explain_points.append(f"\nPut {possible_val} in location {location_readable}.")  
                        
                        if generate_hints:
                                if not hint_grid_outputted:
                                        if int(NUMBER_OF_HINTS) >= int(len(original_empty_cells)):
                                                print(int(len(original_empty_cells)))
                                                print("complete grid has been outputted as the number of hints requested is greater than the number of empty spaces.",attempt)
                                                hint_grid_outputted = True
                        
                    
                    #print(attempt)
                        return attempt

        #reset temp_grid if solution not found, then return false to test next value in parent recursion
        #temp_grid[location[0]][location[1]] = 0
        return False

def recursive_solve(grid, n_rows, n_cols):
        #global spaces_filled
        #global hint_grid_outputted
    
        #N is the maximum integer considered in this board
        n = n_rows*n_cols

        #temp_grid used to test possibles
        temp_grid = copy.deepcopy(grid)

        #print(grid)

        #check if grid full, therefore check if solution found
        #if there are any 0s, the below would return True (not False), meaning there are still empty spaces
        if not any(0 in sublist for sublist in temp_grid):
                if check_solution(grid, n_rows, n_cols):
                        return temp_grid
                return False

        #locate empty cells and store in array of tuples
        empty_cells = []
        row = 0
        index_found = False
        #iterate though rows and columns, if the cell is 0 add location tuple to array
        for row in range(len(temp_grid)):
                for column, cell in enumerate(temp_grid[row]):
                        if cell == 0:
                                location = (row, column)
                                empty_cells.append(location)
        
        #global original_empty_cells
        # original_empty_cells = empty_cells[:] 
        #if not original_empty_cells:
        #    original_empty_cells = copy.deepcopy(empty_cells)
        empty_cell_possibles = []
        #this section checks for what values can go in each empty cell based on duplicates in row/column/box
        for cell_num, location in enumerate(empty_cells): #iterate empty cells, use enumerate to get cell num
                list_pos = []
                for i in range(1,n+1):
                        #check for duplicates within column/row/box
                        #if dup_check(temp_grid, n_rows, n_cols, location, i, n):
                        list_pos.append(i) #add possible value to list
                                
                #add list of possible values for cell to list of values for all empty cells
                empty_cell_possibles.append(list_pos)
        
        # print(empty_cell_possibles)
        #identify least possible values and location of the cell
        least_possible = min(empty_cell_possibles, key=len)
        location = empty_cells[empty_cell_possibles.index(least_possible)]
        #location_readable = tuple(i+1 for i in location)

        #for the least value cell, iterate the possibles and recursive solve for each, returning the solution if found
        for possible_val in least_possible:
                temp_grid[location[0]][location[1]] = possible_val

##                # Section which gives the users hints
##                spaces_filled += 1
##                hint_grids.append(temp_grid)
##                if generate_hints:
##                        if not hint_grid_outputted:
##                                if NUMBER_OF_HINTS == spaces_filled:
##                                        give_solution_hints(NUMBER_OF_HINTS, hint_grids[NUMBER_OF_HINTS - 1])
##                                        hint_grid_outputted = True
                
                attempt = recursive_solve(temp_grid, n_rows, n_cols)
                # print(attempt)
                if attempt:
                        
                        #explanation_points.append(f"\nPut {possible_val} in location {location_readable}.")
                        
##                        if generate_hints:
##                                if not hint_grid_outputted:
##                                        if int(NUMBER_OF_HINTS) >= int(len(original_empty_cells)):
##                                                print(int(len(original_empty_cells)))
##                                                print("complete grid has been outputted as the number of hints requested is greater than the number of empty spaces.",attempt)
##                                                hint_grid_outputted = True
                        
                    
                    #print(attempt)
                        return attempt

        #reset temp_grid if solution not found, then return false to test next value in parent recursion
        #temp_grid[location[0]][location[1]] = 0
        return False

def wavefront_solve(grid, n_rows, n_cols):
        #N is the maximum integer considered in this board
        n = n_rows*n_cols

        #setup some boolean flags to control flow depending on changes
        first_pass = False
        one_pos = False
        no_list = True
        #setup empty list of possible values
        list_of_pos = []
        #iterate trough all cells keeping row and column numbers as variables
        for row in range(len(grid)):
                for column, cell in enumerate(grid[row]):
                        #on first pass we replace 0's with all possible digits and set first pass flag true
                        if cell == 0:
                                grid[row][column] = [i for i in range(1,n+1)]
                                no_list = False
                                first_pass = True
                        #on every other recursion we locate list cells
                        if isinstance(cell, list):
                                new_pos = []
                                #iterate through possible values only keeping the valid ones
                                for pot_val in cell:
                                        if dup_check(grid, n_rows, n_cols, (row,column), pot_val, n):
                                                new_pos.append(pot_val)
                                #if any cells have no valid options, return False to start backtrack
                                if len(new_pos) == 0:
                                        return False
                                #if any cells only have 1 possibility, update the cell to that value
                                if len(new_pos) == 1:
                                        #set one possibility flag true to skip the section for finding minimum later
                                        one_pos = True
                                        new_pos = new_pos[0]
                                #if cell has multiple options, store in list used later to find minimum length cell
                                else:
                                        list_of_pos.append([(row,column),new_pos])
                                        #no list flag false, meaning more recursions until all cells are single value
                                        no_list = False
                                grid[row][column] = new_pos

        #check if we have no definite changes, therefore iterate through smallest possible    
        #also check we arent on first pass when no duplicate checking took place
        if not one_pos and not first_pass:
                min_len = n
                #find the minimum number of possibilities and corresponding location
                for index, location_val_pair in enumerate(list_of_pos):
                        if len(location_val_pair[1]) < min_len:
                                min_len = len(location_val_pair[1])
                                least_pos = list_of_pos[index]
                #iterate through these possibilities, passing deepcopy of grid to wavefront recursion each time
                for val in least_pos[1]:
                        copy_grid = copy.deepcopy(grid)
                        copy_grid[least_pos[0][0]][least_pos[0][1]] = val
                        new_attempt = wavefront_solve(copy_grid, n_rows, n_cols)

                        #check if complete grid returned, or start backtrack
                        if new_attempt:
                                return new_attempt
                return False            

        #if no lists were found, grid must be complete so return grid
        if no_list:
                return grid

        #if at least one value was updated as it was only possible value
        #for location, start next recursion to update other cells as a result
        copy_grid = copy.deepcopy(grid)
        new_attempt = wavefront_solve(copy_grid, n_rows, n_cols)
        if new_attempt:
                return new_attempt
        return False

##def solve(grid, n_rows, n_cols):
##
##        '''
##        Solve function for Sudoku coursework.
##        Comment out one of the lines below to either use the random or recursive solver
##        '''
##        # print(f"grid to solve: {grid}, solution: {recursive_solve(grid, n_rows, n_cols)}")
##        
##        return recursive_solve(grid, n_rows, n_cols)

def sort_terminal_arguments(argvars):
    
    '''
    Process a list of arguments entered from the terminal to determine wheteher 
    an action should be carried out on the grid, the performance of the solver 
    should be analysed, or a process should be explained to the user
   
    arguments: argvars, a list of termnial command line arguments
    returns:    generate_explanation - boolean variable indicating whether an explanation of the solution's steps should be given
                generate_output_file - boolean variable indicating which file to find an unsolved grid from and which file to write the solution to
                fileOUT - a string, giving the name of the new file that the solution should be written to (if the "generate_output_file" variable is true)
                grids -a list of tuples from a file, or from the default global variable, returns the grid to use (and its dimensions)
                generate_hints - boolean variable indicating that N empty spaces of an unsolved grid should be filled correctly
                generate_solution_profile - boolean variable indicating that the performance of the soduko solver should be displayed to the user   
                NUMBER_OF_HINTS - an integer value of the number of hints the user wants the progrma to generate
                
    '''
    
    N_flag_args = 0
    generate_explanation = False
    generate_output_file = False
    global generate_hints
    generate_hints = False
    generate_solution_profile = False
    fileOUT = None
    global NUMBER_OF_HINTS
    NUMBER_OF_HINTS = None
    # global test_grids
    # grids = []
    global grids

    return_dict = {
    "N_flag_args": 0,
    "generate_explanation": False,
    "generate_output_file": False,
    "generate_hints": False,
    "generate_solution_profile": False,
    "fileOUT": None,
    "NUMBER_OF_HINTS": None,
    "grids": []
    }

    
    #Look for valid number of arguments
    flags = [flag for flag in argvars if '-' in flag]
    # print(flags)
    # print(flags, len(flags))
    if len(flags) > MAX_FLAG_CMMDS or len(flags) != len(set(flags)):
        print(f"Only these 4 flags can be entered (each up to once) at any one time. \n\nUSAGE: {USAGE_MESSAGE}")
        # although should we have it so that it can parse multiple file flag inputs?
        exit()
    
    if any(item not in POSSIBLE_FLAGS for item in flags):
        print(f"An invalid flag was entered.\n\nUSAGE: {USAGE_MESSAGE}")
        # although should we have it so that it can parse multiple file flag inputs?
        exit()

    #Look for the explain flag
    if '-explain' in flags:
##        N_flag_args += 1
##        generate_explanation = True

        #return_dict["grids"] = test_grids
        # print(return_dict["grids"])
        return_dict["N_flag_args"] += 1
        return_dict["generate_explanation"] = True

    #Look for the file IN/OUT flag statement
    if '-file' in flags:
        flag_pos = argvars.index('-file')
        if len(argvars[flag_pos:]) >= 3:
            FILES = argvars[flag_pos+1:flag_pos+3]
            # print(FILES)
            fileIN = FILES[0]
            if not os.path.exists(fileIN):
                print(f"The INPUT file entered does not exist. \n\n{USAGE_MESSAGE}")
                exit()
            with open(fileIN, 'r') as f:
                grid_lines = [row.strip('\n') for row in f.readlines()]
            grid_vals = [[int(digit) for digit in row.split(', ')] for row in grid_lines]
            #print(grid_vals, len(grid_vals))
            if len(grid_vals) == 4:
                #grids = [(grid_vals, 2, 2)]
                return_dict["grids"] = [(grid_vals, 2, 2)]
            elif len(grid_vals) == 6:
                #grids = [(grid_vals, 2, 3)]
                return_dict["grids"] = [(grid_vals, 2, 3)]
            elif len(grid_vals) == 9:
                #grids = [(grid_vals, 3, 3)]
                return_dict["grids"] = [(grid_vals, 3, 3)]
                
            else:
                print(f"This solver doesn't support this size of sudoku grid.\n\nUSAGE: {USAGE_MESSAGE}")
                exit()
                
##            fileOUT = FILES[1]
##            N_flag_args += 1
##            generate_output_file = True
            return_dict["fileOUT"] = FILES[1]
            return_dict["N_flag_args"] += 1
            return_dict["generate_output_file"] = True
            
        else:
            print(f"Both an INPUT and OUTPUT files must be entered.\n\nUSAGE: {USAGE_MESSAGE}")
            exit()

    #Look for the hints flag statement
    if '-hint' in flags:
        generate_hints = True
        return_dict["N_flag_args"] += 1
        position_of_number = sys.argv.index("-hint")
        NUMBER_OF_HINTS = int(sys.argv[position_of_number + 1])
    else:
        generate_hints == False

    #Look for the profile flag
    if '-profile' in flags:
        return_dict["grids"] = profile_grids
        # return_dict["grids"] = test_grids
        
        return_dict["N_flag_args"] += 1
        return_dict["generate_solution_profile"] = True

    if '-wavefront' in flags:
        return_dict["N_flag_args"] += 1
        grid_copy = (copy.deepcopy(grids[0][0]),grids[0][1],grids[0][2])
        print(wavefront_solve(grid_copy[0],grid_copy[1],grid_copy[2]))
        

    #Catch error of no (valid) flags
    if return_dict["N_flag_args"] == 0:
        print(f"Please enter a valid flag.\n\nUSAGE: {USAGE_MESSAGE}")
        exit()

    return return_dict
    #return generate_explanation, generate_output_file, fileOUT, grids, generate_hints, NUMBER_OF_HINTS, generate_solution_profile

def write_explanation_to_file(fileOUT):
    explanation_points = SolutionSteps.explain_points
    with open(fileOUT, 'a') as output_file:
        output_file.writelines('\n\nSolution Instructions:')
        if generate_hints:
            output_file.writelines(reversed(explanation_points[-NUMBER_OF_HINTS:]))
        else:
            output_file.writelines(reversed(explanation_points))
    return

def write_solution_to_file(solution, fileOUT):
    solution = [str(row).strip('[]') + '\n' for row in solution]
    with open(fileOUT, 'w+') as output_file:
        output_file.writelines(solution)
    return

def give_solution_hints(N, hint_grid):
    print("The following grid has the first", N, "spaces filled out", hint_grid)
    return

def plot_performance(avg_times):
    
    labels = ['2x2', '2x3', '3x3']

    # Set the width of each bar and the spacing between groups
    bar_size = 0.3

    # Set the positions of the bars for each group
    x_pos1 = np.arange(len(labels))
    x_pos2 = [x + bar_size for x in x_pos1]
    x_pos3 = [x + 2*(bar_size) for x in x_pos1]

    # Plot the bars for each solver
    plt.bar(x_pos1, list(avg_times.values())[0][0], width=bar_size, color='blue', label=str(list(avg_times.keys())[0]))
    plt.bar(x_pos2, list(avg_times.values())[1][0], width=bar_size, color='green', label=str(list(avg_times.keys())[1]))
    plt.bar(x_pos3, list(avg_times.values())[2][0], width=bar_size, color='gray', label=str(list(avg_times.keys())[2]))

    # Add labels and title
    plt.xticks([x + bar_size for x in range(len(labels))], labels)
    
    plt.xlabel('Sudoku Grid Size')
    plt.ylabel('Average solve time (s)')
    plt.title('Sudoku Solver Performance')
    
    plt.legend()
    plt.show()
    
    return


def get_avg_solve_times(solver, grids):
    
    times22 = []
    times23 = []
    times33 = []
    
    for (i, (grid, n_rows, n_cols)) in enumerate(grids):
            
            start_time = time.time()
            solver(grid, n_rows, n_cols)
            # random_solve(grid, n_rows, n_cols)
            elapsed_time = time.time() - start_time
            
            if (n_rows, n_cols) == (2,2):
                times22.append(elapsed_time)
            elif (n_rows, n_cols) == (2,3):
                times23.append(elapsed_time)
            elif (n_rows, n_cols) == (3,3):
                times33.append(elapsed_time)
                
    avg22_time = np.mean(times22)
    avg23_time = np.mean(times23)
    avg33_time = np.mean(times33)
    
    all_times = [times22, times23, times33]
                
    # avg_times = np.array([avg22_time, avg23_time, avg33_time])
    avg_times = np.array([np.mean(i) for i in all_times])
    sdvs = np.array([np.std(i) for i in all_times])
                
    return (avg_times, sdvs)

'''
===================================
DO NOT CHANGE CODE BELOW THIS LINE
===================================
'''
def main(argvars):

        points = 0

        # print("Running test script for coursework 3")
        # print("====================================")
        
        #generate_explanation, generate_output_file, fileOUT, grids, generate_hints, NUMBER_OF_HINTS, generate_solution_profile = sort_terminal_arguments(argvars)
        # print(f"flags tru/not : {sort_terminal_arguments(argvars)}")
        global hint_explanation_points
        global explanation_points
        global original_empty_cells

        re_dict = sort_terminal_arguments(argvars)
        
        if re_dict['generate_solution_profile']:
            
            print("Here is a graph profiling the performance of 3 "\
                  "different solvers in this program"\
                      "\n(All other flags have been ignored)...")
                
            avg_slv_times = {}
            
            avg_slv_times['Random Solve'] =\
                get_avg_solve_times(random_solve, re_dict['grids'])
                
            avg_slv_times['Recursive Solve'] =\
                get_avg_solve_times(random_solve, re_dict['grids'])
                
            avg_slv_times['Improved Recursive Solve'] =\
                get_avg_solve_times(recursive_plus_solve, re_dict['grids'])
            
            plot_performance(avg_slv_times)

        else:
        
            N = re_dict['NUMBER_OF_HINTS']
            
            for (i, (grid, n_rows, n_cols)) in enumerate(re_dict['grids']):
                    # print("Solving grid: %d" % (i+1))

                    hint_explanation_points = []
                    explanation_points = []
                    original_empty_cells = []
                    
                    SolutionSteps.explain_points = []
                    explanation = SolutionSteps.explain_points

                    global hint_grids
                    hint_grids = []
                    global hint_grid_outputted
                    hint_grid_outputted = False
                    # print("Solving grid: %d" % (i+1))
                    hint_explanation_points = []
                    
                    EmptyCells.og_empty_cells = []
                    
                    start_time = time.time()
                    solution = recursive_plus_solve(grid, n_rows, n_cols)
                    
                    elapsed_time = time.time() - start_time
                    
                    if re_dict['generate_hints']:
                        pass
                    
                    if re_dict['generate_output_file']:
                        write_solution_to_file(solution, re_dict['fileOUT'])

                        print(hint_explanation_points)
                        
                        if re_dict['generate_explanation'] or generate_hints:
                            write_explanation_to_file(re_dict['fileOUT'])
                        #if 
                    
                    if re_dict['generate_explanation']\
                        and not re_dict['generate_output_file']:
                        
                        for row in solution:
                            print(row)
                        
                        print(*reversed(explanation))
                        print("\n\n\n")
        
        for (i, (grid, n_rows, n_cols)) in enumerate(grids):
                global spaces_filled
                spaces_filled = 0
                #global hint_grids
                #hint_grids = []
                #global hint_grid_outputted
                #hint_grid_outputted = False
                # print("Solving grid: %d" % (i+1))

                #start_time = time.time()

                #print(grid)
                
                #solution = recursive_plus_solve(grid, n_rows, n_cols)
                #print(solution)
                # print(f"solution: {solution}")
                # if check_solution(solution, n_rows, n_cols):
                #         print("grid %d correct" % (i+1))
                #         points = points + 10
                # else:
                #         print("grid %d incorrect. No solution can be found." % (i+1))
                
                #elapsed_time = time.time() - start_time
                
                # print(len(explanation_points))
                            
                # print(len(explanation_points))
##                if generate_explanation and not generate_output_file:
##                    for row in solution:
##                        print(row)
##                    # print([f"{row}\n" for row in solution])
##                if generate_hints:
##                        print('These are the following ', NUMBER_OF_HINTS, 'moves already filled out:',
##                                *reversed(explanation_points[-NUMBER_OF_HINTS:]))
##                        print("\n\n\n")
##                else:
##                        print(*reversed(explanation_points))
##                        print("\n\n\n")
##                    
##                if generate_solution_profile:
##                    pass
####        
                
            
        # print(grids[:3])
        # print("====================================")
        # print("Test script complete, Total points: %d" % points)


if __name__ == '__main__':
    main(sys.argv[1:])
