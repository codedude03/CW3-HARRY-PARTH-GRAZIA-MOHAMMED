import copy
import time
import sys
import os
import random
import matplotlib.pyplot as plt
import argparse

from pathlib import Path
USAGE_MESSAGE = "Usage: ./CW3_INPUT_OUTPUT.py (-flag). Where -flag is of the\
 formats:\n -explain, -file INPUT_file OUTPUT_file, -hint N, -profile\n\
 or a combination of them all"

MAX_FLAG_CMMDS = 4
POSSIBLE_FLAGS = ['-explain', '-file', '-hint', '-profile']

'''
this is how it works $ python CW3_profile_flag.py -profile easy1.txt easy2.txt
'''

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



def check_section(section, n):
    if len(set(section)) == len(section) and sum(section) == sum([i for i in range(n + 1)]):
        return True
    return False


def get_squares(grid, n_rows, n_cols):
    squares = []
    for i in range(n_cols):
        rows = (i * n_rows, (i + 1) * n_rows)
        for j in range(n_rows):
            cols = (j * n_cols, (j + 1) * n_cols)
            square = []
            for k in range(rows[0], rows[1]):
                line = grid[k][cols[0]:cols[1]]
                square += line
            squares.append(square)

    return squares


def check_solution(grid, n_rows, n_cols):
    '''
    This function is used to check whether a sudoku board has been correctly solved

    args: grid - representation of a suduko board as a nested list.
    returns: True (correct solution) or False (incorrect solution)
    '''
    n = n_rows * n_cols

    for row in grid:
        if check_section(row, n) == False:
            return False

    for i in range(n_rows ** 2):
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
    # function to check for duplicate in row column reduce redundant tests

    # check in row
    if i in grid[location[0]]:
        return False

    # create column list
    column_list = []
    for row in grid:
        column_list.append(row[location[1]])

    # check in column
    if i in column_list:
        return False

    # Calculate which square index returned from get_squares() to consider,
    # by working out position of box that contains location and multiplying
    # number box rows above by number box columns to get index.
    num_vert = n / n_rows
    num_horz = n / n_cols
    square_num = int(int(location[0] / n_rows) * num_horz) + int(location[1] / n_cols)

    # get the squares and identify the square to check in
    squares = get_squares(grid, n_rows, n_cols)
    square = squares[square_num]
    # check in square
    if i in square:
        return False

    # return true if no duplicates found
    return True


original_empty_cells = []


def recursive_solve(grid, n_rows, n_cols):
    # N is the maximum integer considered in this board
    n = n_rows * n_cols

    # temp_grid used to test possibles
    temp_grid = grid

    # check if grid full, therefore check if solution found
    # if there are any 0s, the below would return True (not False), meaning there are still empty spaces
    if not any(0 in sublist for sublist in grid):

        if check_solution(grid, n_rows, n_cols):
            return grid

        return False

    # locate empty cells and store in array of tuples
    empty_cells = []
    row = 0
    index_found = False

    # iterate though rows and columns, if the cell is 0 add location tuple to array
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

    # this section checks for what values can go in each empty cell based on duplicates in row/column/box
    for cell_num, location in enumerate(empty_cells):  # iterate empty cells, use enumerate to get cell num

        list_pos = []
        for i in range(1, n + 1):
            # check for duplicates within column/row/box
            if dup_check(grid, n_rows, n_cols, location, i, n):
                list_pos.append(i)  # add possible value to list

        # add list of possible values for cell to list of values for all empty cells
        empty_cell_possibles.append(list_pos)

    # print(empty_cell_possibles)
    # identify least possible values and location of the cell
    least_possible = min(empty_cell_possibles, key=len)
    location = empty_cells[empty_cell_possibles.index(least_possible)]
    location_readable = tuple(i + 1 for i in location)

    # for the least value cell, iterate the possibles and recursive solve for each, returning the solution if found
    for possible_val in least_possible:

        temp_grid[location[0]][location[1]] = possible_val
        attempt = recursive_solve(temp_grid, n_rows, n_cols)
        # print(attempt)

        if attempt:
            explanation_points.append(f"\nPut {possible_val} in location {location_readable}.")
            return attempt

    # reset temp_grid if solution not found, then return false to test next value in parent recursion
    temp_grid[location[0]][location[1]] = 0

    return False

def sort_terminal_arguments(argvars):

    N_flag_args = 0

    generate_solution_profile = False
    # Looking for a valid number of arguments
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
    file_paths = []
    # Looking for the profile flag
    for arg in argvars:
        if '-profile' in flags:
            N_flag_args += 1
            generate_solution_profile = True
        else:
            file_paths.append(arg)

    # Catch error of no (valid) flags
    if N_flag_args == 0:
        print(f"Please enter a valid flag.\n\nUSAGE: {USAGE_MESSAGE}")
        exit()

    return file_paths, grids, generate_solution_profile

'''
===================================================================
DO NOT CHANGE CODE BELOW PROVIDED CODE FOR COMPARISON PLOT.
===================================================================
'''

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


def recursive_solve_old(grid, n_rows, n_cols):
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

def random_solve(grid, n_rows, n_cols, max_tries=900000000):
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



'''
===================================================================
DO NOT CHANGE CODE ABOVE PROVIDED CODE FOR COMPARISON PLOT.
===================================================================
'''


def get_grid_dimensions(grid):
    n = len(grid)
    if n == 4:
        return (2, 2)
    elif n == 6:
        return (2, 3)
    elif n == 9:
        return (3, 3)
    else:
        raise ValueError("Unsupported grid size.")

def read_file(file_path):
    with open(file_path, 'r') as file:
        grid = []
        for line in file:
            row = [int(x) for x in line.strip().split(',')]
            grid.append(row)
        n_rows, n_cols = get_grid_dimensions(grid)
        return grid, n_rows, n_cols


def measure_time_ns(solver, grid, n_rows, n_cols):
    '''
    This function measures the time of the solvers in nanoseconds.
    Returns the average over a number of iterations set.
    '''
    iterations = 42
    times = []
    # looping over a number of iteration for each of the three solvers.
    for _ in range(iterations):
        # starting the timer in Nanoseconds
        start_time_ns = time.perf_counter_ns()
        solver(grid, n_rows, n_cols)
        times.append(time.perf_counter_ns() - start_time_ns)

    # average over the iterations
    average = (sum(times)) / iterations
    return average

def time_measure(grid_info):
    '''
    this function takes the average for each solver
    '''

    # grid information
    grid, n_rows, n_cols = grid_info

    solvers = [recursive_solve,random_solve, recursive_solve_old]
    averg = []
    for solving in solvers:
        average_time = measure_time_ns(solving, grid, n_rows, n_cols)
        averg.append(average_time)

    return averg


def predefined():
    '''
    This function is used to store the average times of the solvers within a dictionary.
    Returns the values in a dictionary called results
    '''
    averg_info ={"Recursive solver": [],
               "Random solver": [],
               "Old Recursive solver": []}

    # looping through all the grids in the script.
    for (j, grid_info) in enumerate(grids):
        # uses this function to measure the average times
        average_times = time_measure(grid_info)
        # storing each one to there solver.
        averg_info["Recursive solver"].append(average_times[0])
        averg_info["Random solver"].append(average_times[1])
        averg_info["Old Recursive solver"].append(average_times[2])


    results ={}
    # adding them up then dividing by how big the items were.
    for key, value_list in averg_info.items():
        results[key] = sum(value_list)/len(value_list)
    return results

def sorting_grids():
    '''
    This function sorts the grids to their grid size.
    Returns the sorted grids in a dictionary
    '''
    # storing the grid sizes in a dictionry
    sorted_grids = {}

    # going through all the grids in the script
    for grid in grids:
        grid_data, row_size, col_size = grid
        key = (row_size, col_size)

        if key not in sorted_grids:
            sorted_grids[key] = []

        sorted_grids[key].append(grid_data)

    return sorted_grids

def process_input_grids(input_grids):
    '''
    This function takes the inputted grid files and sorts it out.
    Returns the sorted grid of the inputted grids
    '''
    sorted_grids = {}

    # going through all the grids in the for inputted files
    for grid in input_grids:
        grid_data, row_size, col_size = grid
        key = (row_size, col_size)

        if key not in sorted_grids:
            sorted_grids[key] = []

        sorted_grids[key].append(grid_data)

    return sorted_grids



def main(argvars):
    parser = argparse.ArgumentParser(description="Process input files")
    parser.add_argument('-profile', nargs='+', dest='input_files', metavar='FILE', required=True,
                        help='List of input files')
    args = parser.parse_args()

    global explanation_points
    explanation_points = []

    grids,file_paths,generate_solution_profile, = sort_terminal_arguments(argvars)


    if generate_solution_profile:
        # storing the file names and the grids
        input_files = []
        grid_files = []
        for input_file in args.input_files:
            # Process each input file
            input_files.append(Path(input_file).stem)

        for input_file in args.input_files:
            # Process each input file
            grid_files.append(read_file(str(input_file)))
        # storing the averages in this dictionary
        averg_info_file = {"Recursive solver": [],
                      "Random solver": [],
                      "Old Recursive solver": []}

        for i, (grid_info) in enumerate(grid_files):
            average_times = time_measure(grid_info)
            averg_info_file["Recursive solver"].append(average_times[0])
            averg_info_file["Random solver"].append(average_times[1])
            averg_info_file["Old Recursive solver"].append(average_times[2])
        iterations_files = 14
        results_files = {}
        # storing the items as one value when inputting X number of files
        for key, value_list in averg_info_file.items():
            results_files[key] =[value / iterations_files for value in value_list]

        category_grid_size_list = []
        category_grid_size = sorting_grids()
        grid_sizes = list(category_grid_size.keys())
        for grid_size in grid_sizes:
            category_grid_size_list.append(grid_size)

        # solver names that used when sorted
        solver_size = {"Recursive solver": [],
                      "Random solver": [],
                      "Old Recursive solver": []}
        category_grid_size = sorting_grids()
        results_size = {}
        for key_combo, value_list_combo in category_grid_size.items():
            n_rows, n_cols = key_combo
            for grid in value_list_combo:
                grid_info = (grid, n_rows, n_cols)
                average_times = time_measure(grid_info)
                solver_size["Recursive solver"].append(average_times[0])
                solver_size["Random solver"].append(average_times[1])
                solver_size["Old Recursive solver"].append(average_times[2])
        # looping through the items to get an average
        for key, value_list in solver_size.items():
            results_size[key] = sum(value_list) / len(value_list)

        sorted_grids = process_input_grids(grid_files)
        averg_info_file_size = {"Recursive solver": [],
                      "Random solver": [],
                      "Old Recursive solver": []}

        # this is looping to get the average time for the inputted files when sorted
        for grid_size, grid_list in sorted_grids.items():
            for grid in grid_list:
                n_rows, n_cols = grid_size
                average_times = time_measure((grid, n_rows, n_cols))
                averg_info_file_size["Recursive solver"].append(average_times[0])
                averg_info_file_size["Random solver"].append(average_times[1])
                averg_info_file_size["Old Recursive solver"].append(average_times[2])

        # this is when combining both the results_size and results_files into one dictionary
        final_results = {}
        for key in averg_info_file_size:
            value_list_combo = results_size.get(key, None)
            averg_info_file_size_value = averg_info_file_size.get(key, None)

            if value_list_combo is not None and averg_info_file_size_value is not None:
                combined_info = [value_list_combo] + averg_info_file_size_value
                final_results[key] = combined_info
        # when combining the dictionries are add are added together then divided by the size of the item
        final_results_files = {}
        for key, value_list in final_results.items():
            final_results_files[key] = sum(value_list) / len(final_results.items())

        # this is the categories of the plot
        categories_plot = ["2x2"] + ["2x3"] + ["3x3"]
        cate_len = list(range(len(categories_plot)))
        # this is the spacing b/w each category
        total_width = 0.8
        bar_width = total_width / len(final_results_files)
        # this is to keep the 3 bars together and then the next group of bar are plotted
        # next to it.
        offset = -total_width / 2
        for solver, times in final_results_files.items():
            # having the plot to postions the bars into position with their category.
            plt.bar([i + offset for i in cate_len], times, width=bar_width, label=solver)  # label is the legend on the plot.
            offset += bar_width

        # this sets the location along the x-axises for the categories and many there are.
        plt.xticks(cate_len, categories_plot)

        plt.xlabel("Categories")
        plt.ylabel("Average time (in NanoSeconds)")
        plt.title("Performance of Sudoku solvers with inputted files")
        plt.legend()

        # saving the plot as a PNG.
        plt.savefig('Performance grid size.png', dpi=300)
        plt.show()


        #print(solver_size)

        # o = sorting_grids()
        # print(o)
        # print(results_files.items())
        # print(input_files)
        #print(grid_files)
        # a =predefined()
        # x= len(predefined())
        # print(f"\n{a}\n")
        #print(results_final_with_file)
        # z = file_grids(grid_files)
        # print(z)
        # p = len(results_final.items())
        # print(results_final)


if __name__ == '__main__':
    main(sys.argv[1:])


