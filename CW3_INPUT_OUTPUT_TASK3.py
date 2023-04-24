#!/usr/bin/env python3

import copy
import time
import sys
import os
import random
import matplotlib.pyplot as plt
import CW3_sample_grids as sgd
USAGE_MESSAGE = "Usage: ./CW3_INPUT_OUTPUT.py (-flag). Where -flag is of the\
 formats:\n -explain, -file INPUT_file OUTPUT_file, -hint N, -profile\n\
 or a combination of them all"
 # this tells us how to input the arguments
MAX_FLAG_CMMDS = 4
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

        #calculate which square index returned from get_squares() to consider,
        #by working out position of box that contains location and multiplying
        #number box rows above by number box columns to get index.
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
    
original_empty_cells = []

def recursive_solve(grid, n_rows, n_cols):
    
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
        
        global original_empty_cells
        # original_empty_cells = empty_cells[:] 
        if not original_empty_cells:
            original_empty_cells = copy.deepcopy(empty_cells)
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
                attempt = recursive_solve(temp_grid, n_rows, n_cols)
                # print(attempt)
                if attempt:
                    explanation_points.append(f"\nPut {possible_val} in location {location_readable}.")  
                    return attempt

        #reset temp_grid if solution not found, then return false to test next value in parent recursion
        temp_grid[location[0]][location[1]] = 0
        return False

def wavefront_solve(grid, n_rows, n_cols):
    
        #N is the maximum integer considered in this board
        n = n_rows*n_cols

        #temp_grid used to test possibles
        temp_grid = grid

        print(temp_grid)

        #check if grid full, therefore check if solution found
        #if there are any 0s, the below would return True (not False), meaning there are still empty spaces
        first_pass = False
        if any(0 in sublist for sublist in grid):
                first_pass = True

        if first_pass:
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
        
        ##        global original_empty_cells
        ##        # original_empty_cells = empty_cells[:] 
        ##        if not original_empty_cells:
        ##            original_empty_cells = copy.deepcopy(empty_cells)
        #        empty_cell_possibles = []
                #this section checks for what values can go in each empty cell based on duplicates in row/column/box
                for cell_num, location in enumerate(empty_cells): #iterate empty cells, use enumerate to get cell num
                        temp_grid[location[0]][location[1]] = []
        #                list_pos = []
                        for i in range(1,n+1):
                                #check for duplicates within column/row/box
                                if dup_check(grid, n_rows, n_cols, location, i, n):
                                        temp_grid[location[0]][location[1]].append(i) #add possible value to list
        #                                list_pos.append(i)
                        if len(temp_grid[location[0]][location[1]]) == 1:
                                temp_grid[location[0]][location[1]] = temp_grid[location[0]][location[1]][0]
                return wavefront_solve(temp_grid, n_rows, n_cols)
                        #add list of possible values for cell to list of values for all empty cells
        #                empty_cell_possibles.append(list_pos)

        if not first_pass:
                #print('got here')
                no_list = True
                #for row in grid:
                for row in range(len(grid)):
                        for column, cell in enumerate(grid[row]):
                                if isinstance(cell, list):
                                        no_list = False
                if no_list:
                #if not any(isinstance(cell, list) for cell in row):
                        if check_solution(grid, n_rows, n_cols):
                                return grid
                        return False
#continue here idiot
                for row in range(len(grid)):
                        for column, cell in enumerate(grid[row]):
                                if isinstance(cell, list):
                                        location = (row, column)
                                        new_location_values = []
                                        for potential_val in cell:
                                                print(potential_val)
                                                if dup_check(grid, n_rows, n_cols, location, potential_val, n):
                                                        new_location_values.append(potential_val)
                                        if len(new_location_values) == 1:
                                                new_location_values = new_location_values[0]
                                        temp_grid[location[0]][location[1]] = new_location_values
                                                
                attempt = wavefront_solve(temp_grid, n_rows, n_cols)
                if attempt:
                        return attempt
                return False
                
##        # print(empty_cell_possibles)
##        #identify least possible values and location of the cell
##        #least_possible = min(empty_cell_possibles, key=len)
##        least_possible = min(cell for cell in temp_grid if cell > 1, key=len)
##        location = (tempgrid)
####        location_readable = tuple(i+1 for i in location)
##
##        #for the least value cell, iterate the possibles and recursive solve for each, returning the solution if found
##        for possible_val in least_possible:
##                temp_grid[location[0]][location[1]] = possible_val
##                attempt = recursive_solve(temp_grid, n_rows, n_cols)
##                # print(attempt)
##                if attempt:
####                    explanation_points.append(f"\nPut {possible_val} in location {location_readable}.")  
##                    return attempt
##
##        #reset temp_grid if solution not found, then return false to test next value in parent recursion
###        temp_grid[location[0]][location[1]] = 0
##        return False

def solve(grid, n_rows, n_cols):

        '''
        Solve function for Sudoku coursework.
        Comment out one of the lines below to either use the random or recursive solver
        '''
        # print(f"grid to solve: {grid}, solution: {recursive_solve(grid, n_rows, n_cols)}")
        
        return recursive_solve(grid, n_rows, n_cols)

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
    
    N_flag_args = 0
    generate_explanation = False
    generate_output_file = False
    generate_hints = False
    generate_solution_profile = False
    fileOUT = None
    NUMBER_OF_HINTS = None
    # global test_grids
    # grids = []
    global grids

    
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
        N_flag_args += 1
        generate_explanation = True

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
                grids = [(grid_vals, 2, 2)]
            elif len(grid_vals) == 6:
                grids = [(grid_vals, 2, 3)]
            elif len(grid_vals) == 9:
                grids = [(grid_vals, 3, 3)]
                
            else:
                print(f"This solver doesn't support this size of sudoku grid.\n\nUSAGE: {USAGE_MESSAGE}")
                exit()
                
            fileOUT = FILES[1]
            N_flag_args += 1
            generate_output_file = True
        else:
            print(f"Both an INPUT and OUTPUT files must be entered.\n\nUSAGE: {USAGE_MESSAGE}")
            exit()

 	#Look for the hints flag statement
    if '-hint' in flags:
        pass

    #Look for the profile flag
    if '-profile' in flags:
        pass


    if '-wavefront' in flags:
        print(wavefront_solve(grids[0][0],grids[0][1],grids[0][2]))
        

	#Catch error of no (valid) flags
    if N_flag_args == 0:
        print(f"Please enter a valid flag.\n\nUSAGE: {USAGE_MESSAGE}")
        exit()
    
    return generate_explanation, generate_output_file, fileOUT, grids, generate_hints, NUMBER_OF_HINTS, generate_solution_profile

def write_explanation_to_file(fileOUT):
    with open(fileOUT, 'a') as output_file:
        output_file.writelines('\n\nSolution Instructions:')
        output_file.writelines(reversed(explanation_points))
    return

def write_solution_to_file(solution, fileOUT):
    solution = [str(row).strip('[]') + '\n' for row in solution]
    with open(fileOUT, 'w+') as output_file:
        output_file.writelines(solution)
    return

def give_solution_hints(N, solution):
    
    return

def plot_performance(avg_times):
    return

'''
===================================
DO NOT CHANGE CODE BELOW THIS LINE
===================================
'''
def main(argvars):

        points = 0

        # print("Running test script for coursework 3")
        # print("====================================")
        
        generate_explanation, generate_output_file, fileOUT, grids, generate_hints, NUMBER_OF_HINTS, generate_solution_profile = sort_terminal_arguments(argvars)
        # print(f"flags tru/not : {sort_terminal_arguments(argvars)}")
        
        global explanation_points
        global original_empty_cells
        
        
        for (i, (grid, n_rows, n_cols)) in enumerate(grids):
                # print("Solving grid: %d" % (i+1))
                explanation_points = []
                original_empty_cells = []
                start_time = time.time()
                solution = solve(grid, n_rows, n_cols)
                # print(f"solution: {solution}")
                # if check_solution(solution, n_rows, n_cols):
                #         print("grid %d correct" % (i+1))
                #         points = points + 10
                # else:
                #         print("grid %d incorrect. No solution can be found." % (i+1))
                
                elapsed_time = time.time() - start_time
                
                # print(len(explanation_points))
                if generate_hints:
                    pass
                
                if generate_output_file:
                    write_solution_to_file(solution, fileOUT)
                    if generate_explanation:
                        write_explanation_to_file(fileOUT)
                            
                # print(len(explanation_points))
                if generate_explanation and not generate_output_file:
                    for row in solution:
                        print(row)
                    # print([f"{row}\n" for row in solution])
                    print(*reversed(explanation_points))
                    print("\n\n\n")
                    
                if generate_solution_profile:
                    pass
        
                
            
        # print(grids[:3])
        # print("====================================")
        # print("Test script complete, Total points: %d" % points)


if __name__ == '__main__':
	main(sys.argv[1:])
