#!/usr/bin/env python3

import copy
import time
import sys
import os
# import random
# import matplotlib.pyplot as plt
import CW3_sample_grids as sgd

USAGE_MESSAGE = "Usage: ./CW3_INPUT_OUTPUT.py (-flag). Where -flag is of the\
 formats:\n -explain, -file INPUT_file OUTPUT_file, -hint N, -profile\n\
 or a combination of them all"
 # this tells us how to input the arguments
 
MAX_FLAG_CMMDS = 4
POSSIBLE_FLAGS = ['-explain', '-file', '-hint', '-profile']
# should there be a maximum number of flags that can be entered at a time?

grids = sgd.grids

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
        
        #identify least possible values and location of the cell
        least_possible = min(empty_cell_possibles, key=len)
        location = empty_cells[empty_cell_possibles.index(least_possible)]
        location_readable = tuple(i+1 for i in location)

        #for the least value cell, iterate the possibles and recursive solve for each, returning the solution if found
        for possible_val in least_possible:
                temp_grid[location[0]][location[1]] = possible_val
                attempt = recursive_solve(temp_grid, n_rows, n_cols)
                
                if attempt:
                    explanation_points.append(f"\nPut {possible_val} in location {location_readable}.")  
                    return attempt

        #reset temp_grid if solution not found, then return false to test next value in parent recursion
        temp_grid[location[0]][location[1]] = 0
        return False

def solve(grid, n_rows, n_cols):

        '''
        Solve function for Sudoku coursework.
        Comment out one of the lines below to either use the random or recursive solver
        '''
        
        return recursive_solve(grid, n_rows, n_cols)

def sort_terminal_arguments(argvars):
    
    '''
   	Process a list of arguments entered from the terminal to determine wheteher 
    an action should be carried out on the grid, the performance of the solver 
    should be analysed, or a process should be explained to the user
   
   	arguments: argvars - list of termnial command line arguments
   	returns: 	get_explain - boolean variable indicating whether an explanation of the solution's steps should be given
   				get_IO_file - boolean variable indicating which file to find an unsolved grid from and to which file to write the solution
                grids - list of tuples from a file, or from the default global variable, containing the grid to use (and its dimensions)
                get_hints - boolean variable indicating that N empty spaces of an unsolved grid should be revealed
                get_solver_profile - boolean variable indicating that the performance of the soduko solver should be displayed  
                NUMBER_OF_HINTS - integer value of the number of hints the user wants for a grid
                
    '''
    
    N_flag_args = 0
    get_explain = False
    get_IO_file = False
    get_hints = False
    get_solver_profile = False
    fileOUT = None
    NUMBER_OF_HINTS = None
    grids = []

    
    #Look for valid number of arguments
    flags = [flag for flag in argvars if '-' in flag]
    
    if len(flags) > MAX_FLAG_CMMDS or len(flags) != len(set(flags)):
        print("Only these 4 flags can be entered (each up to once) at "\
              f"any one time. \n\nUSAGE: {USAGE_MESSAGE}")
        exit()
    
    if any(item not in POSSIBLE_FLAGS for item in flags):
        print(f"An invalid flag was entered.\n\nUSAGE: {USAGE_MESSAGE}")
        
        exit()

    #Look for the explain flag
    if '-explain' in flags:
        N_flag_args += 1
        get_explain = True

	#Look for the file IN/OUT flag statement
    if '-file' in flags:
        flag_pos = argvars.index('-file')
        
        # check first to see if 2 potetntial valid files have been entered
        if len(argvars[flag_pos:]) >= 3:
            FILES = argvars[flag_pos+1:flag_pos+3]
            fileIN = FILES[0]
            
            # check to see if the input file location exists
            if not os.path.exists(fileIN):
                print("The INPUT file entered does not exist."\
                      f"\n\n{USAGE_MESSAGE}")
                    
                exit()
            
            # reads each line of the 
            with open(fileIN, 'r') as f:
                grid_string = [row.strip('\n') for row in f.readlines()]
                
                
            # turn each value in the list produced from ".split()" to an integer
            grid_list = [[map(int, row.split(', '))] for row in grid_string]
            
            # determine dimensions of the read grid (converted to nested list) 
            if len(grid_list) == 4:
                grids = [(grid_list, 2, 2)]
            if len(grid_list) == 6:
                grids = [(grid_list, 2, 3)]
            if len(grid_list) == 9:
                grids = [(grid_list, 3, 3)]
                
            else:
                print(f"This solver doesn't support this size of sudoku grid.\n\nUSAGE: {USAGE_MESSAGE}")
                exit()
                
            fileOUT = FILES[1]
            N_flag_args += 1
            get_IO_file = True
         
        # exit program if if 2 files are not entered after the '-file' flag
        else:
            print(f"Both an INPUT and OUTPUT files must be entered."\
                  "\n\nUSAGE: {USAGE_MESSAGE}")
            exit()

 	#Look for the hints flag statement
    if '-hint' in flags:
        pass

    #Look for the profile flag
    if '-profile' in flags:
        pass
        

	#Catch error of no (valid) flags being entered
    if N_flag_args == 0:
        print(f"Please enter a valid flag.\n\nUSAGE: {USAGE_MESSAGE}")
        exit()
    
    return get_explain, get_IO_file, fileOUT, grids, get_hints, NUMBER_OF_HINTS, get_solver_profile

'''
===================================
APPLICATION OF PARSED FLAGS:
===================================
'''

def write_explanation_to_file(fileOUT):
    '''
    Writes the explanation of how a full/partial solution was reached to the 
    same file the solution is writtent to
    ----------
    arguments : fileOUT - name and type of file to which the explanation 
                            should be written
    returns: None.
    '''
    
    # append the lines of solution explanation to the already created grid
    with open(fileOUT, 'a') as output_file:
        output_file.writelines('\n\nSolution Instructions:')
        output_file.writelines(reversed(explanation_points))
        
    return

def write_solution_to_file(solution, fileOUT):
    '''
    Convert full/partial solution that was reached to string form, in order to
    write this version of the solution to the a file given by the user.
    ----------
    arguments : solution - nested list, solution grid of integers
                fileOUT - string, name and type of file to which the explanation 
                            should be written
    returns: None.
    '''
    # convert solution to string form
    solution = [str(row).strip('[]') + '\n' for row in solution]
    
    # create a new (or write over an existing) file 
    ##  and write each line of the string version to the file
    with open(fileOUT, 'w+') as output_file:
        output_file.writelines(solution)
        
    return

def give_solution_hints(N, solution):
        
    return

def plot_performance(avg_times):
    #matplotlib?
    return

'''
===================================
DO NOT CHANGE CODE BELOW THIS LINE
===================================
'''
def main(argvars):

        points = 0

        print("Running test script for coursework 3")
        print("====================================")
        
        get_explain, get_IO_file, fileOUT, grids, get_hints, NUMBER_OF_HINTS, get_solver_profile = sort_terminal_arguments(argvars)
        
        global explanation_points
        global original_empty_cells
        # make these variables global in order to edit them in this function
        
        # N = NUMBER_OF_HINTS
        
        for (i, (grid, n_rows, n_cols)) in enumerate(grids):
            
                explanation_points = []
                original_empty_cells = []
                # reset these varaibles to empty lists before solving each new grid
                
                start_time = time.time()
                solution = solve(grid, n_rows, n_cols)
                
                # this is simply to see whats happening to the grids while editing
                print(f"\nsolution: {solution}")
                if check_solution(solution, n_rows, n_cols):
                        print("grid %d correct" % (i+1))
                        points = points + 10
                else:
                        print("grid %d incorrect. No solution can be found." % (i+1))
                
                elapsed_time = time.time() - start_time
                
                if get_hints:
                    # N number of hints used in a seperate function above?
                    # probably just print to terminal if not asked to write to file??:
                    # if not not generate_output_file:
                    pass
                
                if get_IO_file:
                    write_solution_to_file(solution, fileOUT)
                    if get_explain:
                        write_explanation_to_file(fileOUT)
                            
                if get_explain and not get_IO_file:
                    for row in solution:
                        print(row)
                        
                    # reversed so that the first empty space filled is explained first (for the recursive function)
                    # may have to change this for the wavefront solver? if explanations saved in the correct order
                    print(*reversed(explanation_points))
                    print("\n\n\n")
                    
                if get_solver_profile:
                    # something to do with average timing - so, make sure time function only records solver time
                    ## i.e. don't include user input time
                    pass
         
        print("====================================")
        print("Test script complete, Total points: %d" % points)


if __name__ == '__main__':
	main(sys.argv[1:])
