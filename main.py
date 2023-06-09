#!/usr/bin/env python3

import copy
import time
import sys
import os
import random
import matplotlib.pyplot as plt
import numpy as np
USAGE_MESSAGE = "Usage: ./CW3_FINAL_FINAL.py (-flag). Where -flag is of the\
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

'''
===================================
DO NOT CHANGE CODE ABOVE THIS LINE
===================================
'''
def check_section(section, n):
    #check a section e.g a row, column or box

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

#class to create emptycells object to store empty cells
class EmptyCells:
    # class variable storing all empty cells of the grid originally given
    og_empty_cells = []
    
    def __init__(self, x):
        self.x = x
        EmptyCells.og_empty_cells = self  # Set the instance as a class variable
    
    def __str__(self):
        return str(self.x)

#class to create SolutionSteps object to store Solution Steps
class SolutionSteps:
    # class variable storing all movements made to produce partial/full solved grid
    explain_points = []
    
    def __init__(self, x):
        self.x = x
        SolutionSteps.explain_points = self  # Set the instance as a class variable
    
    def __str__(self):
        return str(self.x)


def get_og_empty_cells(empty_cells):
    # only saves a list of empty cells from the starting grid (unchanged after first update in a recursion)
    if not EmptyCells.og_empty_cells:
        EmptyCells.og_empty_cells = empty_cells
    
    return

def dup_check(grid_to_check, n_rows, n_cols, location, num, n):
        '''
        function to check for duplicate in row, column, 
        box to reduce redundant tests
        
        args: grid - sudoku grid as nested list
              n_rows & n_cols - grid dimensions
              location - tuple of empty cell coordinate
              num - the number being compared to check for possible duplicates
              n - size of grid
        return: Boolean true/false - True if no duplicate found
        
        '''

        #check in row
        if num in grid_to_check[location[0]]:
                return False
        
        #create column list
        column_list = []
        for row in grid_to_check:
                column_list.append(row[location[1]])
        #check in column
        if num in column_list:
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
        if num in square:
                return False

        #return true if no duplicates found
        return True


original_empty_cells = []
#define the number of spaces filled to be preset to 0
global spaces_filled
spaces_filled = 0


def random_solve(grid, n_rows, n_cols, max_tries=10000):
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

        #randomly try combinations in range
        for i in range(max_tries):
                possible_solution = fill_board_randomly(grid, n_rows, n_cols)
                if check_solution(possible_solution, n_rows, n_cols):
                        return possible_solution

        return grid


def recursive_plus_solve(grid, n_rows, n_cols):
        global spaces_filled
        global hint_grid_outputted
        # n is the maximum integer considered in this board
        n = n_rows*n_cols

        #temp_grid used to test possibles
        temp_grid = copy.deepcopy(grid)

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

        #store empty cells in class variable
        get_og_empty_cells(empty_cells)
                                
        empty_cell_possibles = []
        #this section checks for what values can go in each empty cell based on duplicates in row/column/box
        for cell_num, location in enumerate(empty_cells): #iterate empty cells, use enumerate to get cell num
                list_pos = []
                for num in range(1,n+1):
                        #check for duplicates within column/row/box
                        if dup_check(temp_grid, n_rows, n_cols, location, num, n):
                                list_pos.append(num) #add possible value to list
                                
                #add list of possible values for cell to list of values for all empty cells
                empty_cell_possibles.append(list_pos)
        
        #identify least possible values and location of the cell
        least_possible = min(empty_cell_possibles, key=len)
        location = empty_cells[empty_cell_possibles.index(least_possible)]
        location_readable = tuple(i+1 for i in location)

        #for the least value cell, iterate the possibles and recursive solve for each, returning the solution if found
        for possible_val in least_possible:
                temp_grid[location[0]][location[1]] = possible_val
                #increases the  of spaces filled
                spaces_filled += 1
                #List of grids which have each move in them 
                hint_grids.append(temp_grid)
                attempt = recursive_plus_solve(temp_grid, n_rows, n_cols)
                if attempt:
                    # for the final value entered, save its coordinates to class variable
                    SolutionSteps.explain_points.append(f"\nPut {possible_val} "\
                                                        f"in location {location_readable}.")

                    return attempt

        #reset temp_grid if solution not found, then return false to test next value in parent recursion
        #temp_grid[location[0]][location[1]] = 0
        return False

def recursive_solve(grid, n_rows, n_cols):
    
        #N is the maximum integer considered in this board
        n = n_rows*n_cols

        #temp_grid used to test possibles
        temp_grid = copy.deepcopy(grid)


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
        
        empty_cell_possibles = []
        #this section checks for what values can go in each empty cell based on duplicates in row/column/box
        for cell_num, location in enumerate(empty_cells): #iterate empty cells, use enumerate to get cell num
                list_pos = []
                for num in range(1,n+1):
                        #in improved version we check for duplicates here
                        list_pos.append(num) #add possible value to list
                                
                #add list of possible values for cell to list of values for all empty cells
                empty_cell_possibles.append(list_pos)
        
        #identify least possible values and location of the cell
        least_possible = min(empty_cell_possibles, key=len)
        location = empty_cells[empty_cell_possibles.index(least_possible)]

        #for the least value cell, iterate the possibles and recursive solve for each, returning the solution if found
        for possible_val in least_possible:
                temp_grid[location[0]][location[1]] = possible_val
                
                attempt = recursive_solve(temp_grid, n_rows, n_cols)
                if attempt:
                        return attempt
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
        #use a deepcopy to prevent backtracking errors
        copy_grid = copy.deepcopy(grid)
        new_attempt = wavefront_solve(copy_grid, n_rows, n_cols)
        if new_attempt:
                return new_attempt
        return False


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

    #setup some globals for setting different flags true or false
    global generate_hints
    generate_hints = False
    global NUMBER_OF_HINTS
    NUMBER_OF_HINTS = None
    global grids
    
    #setup dictionary of booleans to singal flag conditions
    return_dict = {
    "N_flag_args": 0,
    "generate_explanation": False,
    "generate_output_file": False,
    "generate_hints": False,
    "generate_solution_profile": False,
    "fileOUT": None,
    "NUMBER_OF_HINTS": None,
    "grids": grids
    }
    
    if return_dict["generate_hints"] == True:
        generate_hints = True
    
    #Look for valid number of arguments
    flags = [flag for flag in argvars if '-' in flag]
    if len(flags) > MAX_FLAG_CMMDS or len(flags) != len(set(flags)):
        print(f"Only these 4 flags can be entered (each up to once) at any one time. \n\nUSAGE: {USAGE_MESSAGE}")
        exit()
    
    # exits program if any of the flag ('-flag' format) is not recognised
    if any(item not in POSSIBLE_FLAGS for item in flags):
        print(f"An invalid flag was entered.\n\nUSAGE: {USAGE_MESSAGE}")
        exit()

    #Look for the explain flag
    if '-explain' in flags:
        return_dict["N_flag_args"] += 1
        return_dict["generate_explanation"] = True

    #Look for the file IN/OUT flag statement
    if '-file' in flags:
        flag_pos = argvars.index('-file')
        if len(argvars[flag_pos:]) >= 3:
            FILES = argvars[flag_pos+1:flag_pos+3]
            
            fileIN = FILES[0]
            if not os.path.exists(fileIN):
                print(f"The INPUT file entered does not exist. \n\n{USAGE_MESSAGE}")
                exit()
            
            with open(fileIN, 'r') as f:
                grid_lines = [row.strip('\n') for row in f.readlines()]
            
            grid_vals = [[int(digit) for digit in row.split(', ')] for row in grid_lines]
            
            if len(grid_vals) == 4:
                return_dict["grids"] = [(grid_vals, 2, 2)]
                
            elif len(grid_vals) == 6:
                return_dict["grids"] = [(grid_vals, 2, 3)]
                
            elif len(grid_vals) == 9:
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
        return_dict["generate_hints"] = True
        return_dict["N_flag_args"] += 1
        position_of_number = argvars.index('-hint')
        NUMBER_OF_HINTS = int(argvars[position_of_number + 1])
    else:
        return_dict["generate_hints"] = False


    #Look for the profile flag
    if '-profile' in flags:
        return_dict["grids"] = grids
        
        return_dict["N_flag_args"] += 1
        return_dict["generate_solution_profile"] = True

    if '-wavefront' in flags:
        print('Solving using wavefront')
        for grid in grids:        
            grid_copy = (copy.deepcopy(grid[0]),grid[1],grid[2])
            start_time = time.time()
            solution = wavefront_solve(grid_copy[0],grid_copy[1],grid_copy[2])
            elapsed_time = time.time() - start_time
            print('Solution:',*solution,'solved in ' + str(elapsed_time) + ' seconds', sep='\n')  
        return_dict["N_flag_args"] += 1
        

    #run default if no flags given
    if return_dict["N_flag_args"] == 0:
        print('solving hardcoded grids using improved recursion')
        for grid in grids:
            start_time = time.time()
            solution = recursive_plus_solve(grid[0],grid[1],grid[2])
            elapsed_time = time.time() - start_time
            print('Solution:',*solution,'solved in ' + str(elapsed_time) + ' seconds', sep='\n')
            print(recursive_plus_solve(grid[0],grid[1],grid[2]))
        
        exit()

    return return_dict



def write_explanation_to_file(fileOUT):
    '''
    Function to produce an output file of the solution to the grid in an input
    file provided, taking the new file's name as an argument.

    '''
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


#Function which outputs the hint grid.
def give_solution_hints(N, hint_grid):
    hint_grid = np.array([row for row in hint_grid])
    
    print("\n\nThe following grid has the first", N, "spaces filled out:")
    print(hint_grid)
    return


#function which outputs the full solution when number of hints would output the entire solution
def give_full_solution(hint_grid):
    print("\n\nComplete grid has been outputted as the number of hints "\
          "requested greater than the number of empty spaces:")
    
    hint_grid = np.array([row for row in hint_grid])
    print (hint_grid)
    
    return


def plot_performance(avg_times):
    '''
    This function is used to plot the average time in seconds verse the grid size of
    the sudoku solver used in the script; taking the dictionary of average times
    for each solver as the argument.
    '''

    print('Plotting average perforance of random, recursive and wavefront. This may take up to 20 seconds')

    # Category labelling for the plot
    labels = ['2x2', '2x3', '3x3']
    
    # Creating a log scale for the y-axis
    plt.yscale('log')

    # Set the width of each bar and the spacing between groups
    bar_size = 0.3

    # Set the positions of the bars for each group
    
    x_pos1 = np.arange(len(labels))
    # ^^creates evenly spaced positions in array of coordinates used to plot
    x_pos2 = [x + bar_size for x in x_pos1]
    x_pos3 = [x + 2*(bar_size) for x in x_pos1]
    # ^^create 3 different starting positions for the three solvers' bars

    # Plot and format the bars for each solver
    keys = list(avg_times.keys())
    values = list(avg_times.values())
    plt.bar(x_pos1, values[0], 
            width=bar_size, color='blue',
            label=str(keys[0]))
    
    plt.bar(x_pos2, values[1],
            width=bar_size, color='green',
            label=str(keys[1]))
    
    plt.bar(x_pos3, values[2],
            width=bar_size, color='gray', 
            label=str(keys[2]))
    
    # Add x-axis markers, labels and title
    plt.xticks([x + bar_size for x in range(len(labels))], labels)
    
    plt.xlabel('Sudoku Grid Size')
    plt.ylabel('Log [Average Solve Time (s)]')
    plt.title('Sudoku Solver Performance')

    # Save graph plotted as a pdf to the directory
    plt.savefig("Performance.png",dpi=300)
    plt.legend()
    plt.show()
    
    return


def get_avg_solve_times(solver, grids):
    
    times22 = []
    times23 = []
    times33 = []

    # iterating through the grids in the script
    for (i, (grid, n_rows, n_cols)) in enumerate(grids):

            # starting the timer for that grid
            start_time = time.time()

            # Parameter used to go through all the solvers in the script.
            solver(grid, n_rows, n_cols)
            # random_solve(grid, n_rows, n_cols)

            # difference between the start and end time
            elapsed_time = time.time() - start_time

            # sorting the grid sizes for the elapsed_time of that grid used.
            if (n_rows, n_cols) == (2,2):
                times22.append(elapsed_time)
            elif (n_rows, n_cols) == (2,3):
                times23.append(elapsed_time)
            elif (n_rows, n_cols) == (3,3):
                times33.append(elapsed_time)
                
    avg22_time = np.mean(times22)
    avg23_time = np.mean(times23)
    avg33_time = np.mean(times33)

    # storing all the times recording when elapsed_time for each grid size as a sub-list
    all_times = [times22, times23, times33]
                
    # calculating the average for all the grid by iterating over the sub-list of all_times
    avg_times = np.array([np.mean(i) for i in all_times])
                
    return (avg_times)

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
        
        global hint_grids
        hint_grids = []
        
        re_dict = sort_terminal_arguments(argvars)
        if re_dict['generate_solution_profile']:
            print("\n\nHere is a graph profiling the performance of 3 "\
                  "different solvers in this program"\
                      "\n(All other flags have been ignored)...\n")

            # storing the average of the different solvers and size of the grids as a dictionay.
            avg_slv_times = {}

            # adding the random solver variables to the dictionay
            avg_slv_times['Random Solve'] =\
                get_avg_solve_times(random_solve, re_dict['grids'])
                
            #avg_slv_times['Recursive Solve'] =\
             #   get_avg_solve_times(random_solve, re_dict['grids'])

            # adding the Improved recursive solver variables to the dictionay
            avg_slv_times['Improved Recursive Solve'] =\
                get_avg_solve_times(recursive_plus_solve, re_dict['grids'])

            # adding the wavefront solver variables to the dictionay
            avg_slv_times['Wavefront Solve'] =\
                get_avg_solve_times(wavefront_solve, re_dict['grids'])            

            # using this function it plot the data that is stored in the dictionay.
            plot_performance(avg_slv_times)

        else:
            N = re_dict['NUMBER_OF_HINTS']
            #for (i, (grid, n_rows, n_cols)) in enumerate(re_dict['grids']):
            for (i, (grid, n_rows, n_cols)) in enumerate(grids):
                global spaces_filled
                spaces_filled = 0
                #variable checks if a hint has already been outputted
                global hint_grid_outputted
                hint_grid_outputted = False
                hint_grids = []
                explanation_points = []
                original_empty_cells = []
                    
                # Resets the class variable 'explain_points' before solving each grid
                SolutionSteps.explain_points = []
                explanation = SolutionSteps.explain_points
                
                # Resets the class variable here before solving each grid
                EmptyCells.og_empty_cells = []
                    
                solution = recursive_plus_solve(grid, n_rows, n_cols)
                    
                #section for hint flag
                if re_dict['generate_hints']\
                    and not re_dict['generate_output_file']:
                    if NUMBER_OF_HINTS < spaces_filled:
                        
                        #call function dependent on whether full solution or partial solution is required
                        give_solution_hints(NUMBER_OF_HINTS, hint_grids[NUMBER_OF_HINTS - 1])
                        
                    else:
                        give_full_solution(hint_grids[-1:])

                if re_dict['generate_output_file']:
                    write_solution_to_file(solution, re_dict['fileOUT'])
                        
                    if re_dict['generate_explanation'] or re_dict["generate_hints"]:
                        write_explanation_to_file(re_dict['fileOUT'])
                    
                # Print explanation to terminal
                solution = np.array([num for num in row] for row in solution)
                if re_dict['generate_explanation']\
                    and not re_dict['generate_output_file']:
                        
                    #explain with hints
                    if re_dict['generate_hints']:
                        print('These are the following moves already filled out:')
                        print(*reversed(explanation[-NUMBER_OF_HINTS:]))
                        
                    #explain without hints
                    else:
                        print(solution)
                        print('These are the moves used to obtain the solution',*reversed(explanation))
                        print("\n\n\n")


if __name__ == '__main__':
    main(sys.argv[1:])
