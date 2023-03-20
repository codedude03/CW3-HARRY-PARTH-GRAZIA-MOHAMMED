import copy
import time

#Grids 1-5 are 2x2
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
		[6, 1, 9, 8, 4, 2, 5, 3, 7,],
		[7, 0, 5, 3, 6, 9, 1, 8, 2,],
		[8, 3, 2, 1, 7, 5, 0, 0, 9,],
		[1, 5, 8, 6, 9, 7, 3, 2, 4,],
		[0, 6, 4, 2, 0, 1, 8, 7, 5,],
		[2, 0, 3, 0, 8, 4, 6, 9, 1,],
		[4, 0, 7, 9, 5, 6, 2, 0, 3,],
		[3, 9, 1, 4, 0, 0, 7, 5, 6,],
		[5, 2, 0, 7, 1, 3, 9, 4, 8,]]

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

        for i in range(n_rows):
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

def recursive_solve(grid, n_rows, n_cols):

        def dup_check(grid, n_rows, n_cols, location, i):
                #function to check for duplicate in row column reduce redundant tests
                if i in grid[location[0]]:
                        return False
                column_list = []
                for row in grid:
                        column_list.append(row[location[1]])
                if i in column_list:
                        return False
                return True
        
        #N is the maximum integer considered in this board
        n = n_rows*n_cols
        
        temp_grid = grid

        #check if grid full, therefore check if solution found
        if not any(0 in sublist for sublist in grid):
                if check_solution(grid, n_rows, n_cols):
                        return grid
                return False

        #locate first empty cell
        row = 0
        index_found = False
        while not index_found:
                if 0 in grid[row]:
                        column = grid[row].index(0)
                        location = (row, column)
                        index_found = True
                row += 1


        for i in range(1,n+1):
                # check for duplicates in row/column to avoid redundant tests - without massively increases time
                if dup_check(grid, n_rows, n_cols, location, i):
                        #update temp_grid with the new value
                        temp_grid[location[0]][location[1]] = i
                        attempt = recursive_solve(temp_grid, n_rows, n_cols)
                        if attempt:
                                return attempt
        temp_grid[location[0]][location[1]] = 0
        return False


def random_solve(grid, n_rows, n_cols, max_tries=500):
        
        for i in range(max_tries):
                pass

        return grid


def solve(grid, n_rows, n_cols):

        '''
        Solve function for Sudoku coursework.
        Comment out one of the lines below to either use the random or recursive solver
        '''
        
        #return random_solve(grid, n_rows, n_cols)
        return recursive_solve(grid, n_rows, n_cols)


'''
===================================
DO NOT CHANGE CODE BELOW THIS LINE
===================================
'''
def main():

        points = 0

        print("Running test script for coursework 1")
        print("====================================")
        
        for (i, (grid, n_rows, n_cols)) in enumerate(grids):
                print("Solving grid: %d" % (i+1))
                start_time = time.time()
                solution = solve(grid, n_rows, n_cols)
                elapsed_time = time.time() - start_time
                print("Solved in: %f seconds" % elapsed_time)
                print(solution)
                if check_solution(solution, n_rows, n_cols):
                        print("grid %d correct" % (i+1))
                        points = points + 10
                else:
                        print("grid %d incorrect" % (i+1))

        print("====================================")
        print("Test script complete, Total points: %d" % points)


if __name__ == "__main__":
        main()
