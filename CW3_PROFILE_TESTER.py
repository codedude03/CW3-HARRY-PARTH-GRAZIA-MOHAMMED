#!/usr/bin/env python3

import copy
import time
import sys
import os
import random
import numpy as np
import matplotlib.pyplot as plt
import CW3_sample_grids as sgd
USAGE_MESSAGE = "Usage: ./CW3_INPUT_OUTPUT.py (-flag). Where -flag is of the\
 formats:\n -explain, -file INPUT_file OUTPUT_file, -hint N, -profile\n\
 or a combination of them all"
 # this tells us how to input the arguments
MAX_FLAG_CMMDS = 4
POSSIBLE_FLAGS = ['-explain', '-file', '-hint', '-profile']

test_grids = sgd.default_grids
profile_grids = sgd.profile_grids_1
# print(test_grids)
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


def dup_check(grid, n_rows, n_cols, location, i, n):
        #function to check for duplicate in row column reduce redundant tests
        
        #check in row
        if i in grid[location[0]]:
                return False
        
        #create column list
        column_list = []
        for row in grid:
                column_list.append(row[location[1]])
        #check in column
        if i in column_list:
                return False

        #calculate which square index returned from get_squares() to consider, by working out position of box that contains location and multiplying number box rows above by number box columns to get index
        num_vert = n/n_rows
        num_horz = n/n_cols
        square_num = int(int(location[0]/n_rows)*num_horz) + int(location[1]/n_cols)
        #get the squares and identify the square to check in
        squares = get_squares(grid, n_rows, n_cols)
        square = squares[square_num]
        #check in square
        if i in square:
                return False

        #return true if no duplicates found
        return True


def recursive_plus_solve(grid, n_rows, n_cols):
    
        #N is the maximum integer considered in this board
        n = n_rows*n_cols

        #temp_grid used to test possibles
        temp_grid = grid

        #check if grid full, therefore check if solution found
        #if there are any 0s, the below would return True (not False), meaning there are still empty spaces
        if not any(0 in sublist for sublist in grid):
                if check_solution(grid, n_rows, n_cols):
                        return grid
                return False

        #locate empty cells and store in array of tuples
        empty_cells = []
        row = 0
        index_found = False
        #iterate though rows and columns, if the cell is 0 add location tuple to array
        for row in range(len(grid)):
                for column, cell in enumerate(grid[row]):
                        if cell == 0:
                                location = (row, column)
                                empty_cells.append(location)
        
        # global original_empty_cells
        # original_empty_cells = empty_cells[:] 
        
        get_og_empty_cells(empty_cells)
        
        # print(get_og_empty_cells(empty_cells))
        
        # if not original_empty_cells:
        #     original_empty_cells = copy.deepcopy(empty_cells)
        empty_cell_possibles = []
        #this section checks for what values can go in each empty cell based on duplicates in row/column/box
        for cell_num, location in enumerate(empty_cells): #iterate empty cells, use enumerate to get cell num
                list_pos = []
                for i in range(1,n+1):
                        #check for duplicates within column/row/box
                        if dup_check(grid, n_rows, n_cols, location, i, n):
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
                attempt = recursive_plus_solve(temp_grid, n_rows, n_cols)
                # print(attempt)
                if attempt:
                    SolutionSteps.explain_points.append(f"\nPut {possible_val} in location {location_readable}.")  
                    return attempt

        #reset temp_grid if solution not found, then return false to test next value in parent recursion
        temp_grid[location[0]][location[1]] = 0
        return False
    

def find_empty(grid):
	'''
	This function returns the index (i, j) to the first zero element in a sudoku grid
	If no such element is found, it returns None

	args: grid
	return: A tuple (i,j) where i and j are both integers, or None
	'''

	for i in range(len(grid)):
		row = grid[i]
		for j in range(len(row)):
			if grid[i][j] == 0:
				return (i, j)

	return None


def recursive_solve(grid, n_rows, n_cols):
	'''
	This function uses recursion to exhaustively search all possible solutions to a grid
	until the solution is found

	args: grid, n_rows, n_cols
	return: A solved grid (as a nested list), or None
	'''

	#N is the maximum integer considered in this board
	n = n_rows*n_cols
	#Find an empty place in the grid
	empty = find_empty(grid)

	#If there's no empty places left, check if we've found a solution
	if not empty:
		#If the solution is correct, return it.
		if check_solution(grid, n_rows, n_cols):
			return grid 
		else:
			#If the solution is incorrect, return None
			return None
	else:
		row, col = empty 

	#Loop through possible values
	for i in range(1, n+1):

			#Place the value into the grid
			grid[row][col] = i
			#Recursively solve the grid
			ans = recursive_solve(grid, n_rows, n_cols)
			#If we've found a solution, return it
			if ans:
				return ans 

			#If we couldn't find a solution, that must mean this value is incorrect.
			#Reset the grid for the next iteration of the loop
			grid[row][col] = 0 

	#If we get here, we've tried all possible values. Return none to indicate the previous value is incorrect.
	return None

def random_solve(grid, n_rows, n_cols, max_tries=50000):
	'''
	This function uses random trial and error to solve a Sudoku grid

	args: grid, n_rows, n_cols, max_tries
	return: A solved grid (as a nested list), or the original grid if no solution is found
	'''

	for i in range(max_tries):
		possible_solution = fill_board_randomly(grid, n_rows, n_cols)
		if check_solution(possible_solution, n_rows, n_cols):
			return possible_solution

	return grid

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


def solve(grid, n_rows, n_cols):

        '''
        Solve function for Sudoku coursework.
        Comment out one of the lines below to either use the random or recursive solver
        '''
        
        return recursive_plus_solve(grid, n_rows, n_cols)
        # return random_solve(grid, n_rows, n_cols),\
        #     recursive_solve(grid, n_rows, n_cols),\
        #         recursive_solve_plus(grid, n_rows, n_cols)

def sort_terminal_arguments(argvars):
    
    '''
   	Process a list of arguments entered from the terminal to determine wheteher 
    an action should be carried out on the grid, the performance of the solver 
    should be analysed, or a process should be explained to the user
   
   	arguments: argvars, a list of termnial command line arguments
   	returns: 	generate_explanation - boolean variable indicating whether an explanation of the solution's steps should be given
   				generate_output_file - boolean variable indicating which file to find an unsolved grid from and which file to write the solution to
   				fileOUT - a string, giving the name of the new file that the solution should be written to (if the "generate_output_file" variable is true)
                grids -a list of tuples from a file, or from the default global variable, returns the grid to use (and its dimensions)
                generate_hints - boolean variable indicating that N empty spaces of an unsolved grid should be filled correctly
                generate_solution_profile - boolean variable indicating that the performance of the soduko solver should be displayed to the user   
                NUMBER_OF_HINTS - an integer value of the number of hints the user wants the progrma to generate
                
    '''
    
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
        return_dict["grids"] = test_grids
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
            if len(grid_vals) == 4:
                return_dict["grids"] = [(grid_vals, 2, 2)]
            if len(grid_vals) == 6:
                return_dict["grids"] = [(grid_vals, 2, 3)]
            if len(grid_vals) == 9:
                return_dict["grids"] = [(grid_vals, 3, 3)]
                
            else:
                print(f"This solver doesn't support this size of sudoku grid.\n\nUSAGE: {USAGE_MESSAGE}")
                exit()
                
            return_dict["fileOUT"] = FILES[1]
            return_dict["N_flag_args"] += 1
            return_dict["generate_output_file"] = True
        else:
            print(f"Both an INPUT and OUTPUT files must be entered.\n\nUSAGE: {USAGE_MESSAGE}")
            exit()

 	#Look for the hints flag statement
    if '-hint' in flags:
        pass

    #Look for the profile flag
    if '-profile' in flags:
        
        return_dict["grids"] = profile_grids
        # return_dict["grids"] = test_grids
        
        return_dict["N_flag_args"] += 1
        return_dict["generate_solution_profile"] = True
        

	#Catch error of no (valid) flags
    if return_dict["N_flag_args"] == 0:
        print(f"Please enter a valid flag.\n\nUSAGE: {USAGE_MESSAGE}")
        exit()
    
    return return_dict



def write_explanation_to_file(fileOUT):
    explanation = SolutionSteps.explain_points
    with open(fileOUT, 'a') as output_file:
        output_file.writelines('\n\nSolution Instructions:')
        output_file.writelines(reversed(explanation))
    return

def write_solution_to_file(solution, fileOUT):
    solution = [str(row).strip('[]') + '\n' for row in solution]
    with open(fileOUT, 'w+') as output_file:
        output_file.writelines(solution)
    return

def give_solution_hints(N, solution):
    
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
                    
                    SolutionSteps.explain_points = []
                    explanation = SolutionSteps.explain_points
                    
                    EmptyCells.og_empty_cells = []
                    
                    start_time = time.time()
                    solution = solve(grid, n_rows, n_cols)
                    
                    elapsed_time = time.time() - start_time
                    
                    if re_dict['generate_hints']:
                        pass
                    
                    if re_dict['generate_output_file']:
                        write_solution_to_file(solution, re_dict['fileOUT'])
                        if re_dict['generate_explanation']:
                            write_explanation_to_file(re_dict['fileOUT'])
                    
                    if re_dict['generate_explanation']\
                        and not re_dict['generate_output_file']:
                        
                        for row in solution:
                            print(row)
                        
                        print(*reversed(explanation))
                        print("\n\n\n")
                        
            
        # print(grids[:3])
        # print("====================================")
        # print("Test script complete, Total points: %d" % points)


if __name__ == '__main__':
	main(sys.argv[1:])
