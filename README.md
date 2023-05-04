# CW3-HARRY-PARTH-GRAZIA-MOHAMMED
CW3 python file to solve all size sudokus as efficiently as possible.

This is a Python script for a Sudoku solver program. The program uses three technqiues to solve the sudoku grids as efficiently as possible. The program runs in the Git bash terminal.

Follow the steps below to the run the program properly:

1- Download the least version of Python from the Web in to you PC.

2- Once Downloaded, Click on the "Add Python 3.11.3 to PATH" in the installer window then Click on install now. Note that "3.11.3" numbers maybe different for yours so no need to worry about that.

3-In Git bash navigate to the file called "CW3_HARRY_PARTH_GRAZIA_MOHAMMED" from your PC.

4- Open and run the Program "CW3_FINAL_FINAL.py" using a software that run Python scripts.

5- Install the matplotlib libary if you haven't, using "pip install matplotlib".

6- Install the numpy libary if you haven't, using "pip install numpy".



Project features:

It is an open-source program and simple to use.

The program supports for the grid sizes of 2x2, 2x3 and 3x3.

Includes grids in the script and within files provided with increasing difficulty.

Includes flags that are called in the Git bash terminal.

Using flags it produces solutions, hints, and explain of a grid as well as a plot of the performance of the solvers in the script.

There is an additional flag called wavefront which is representing the smallest possible values for each grid location within a grid.



Project usage of the implemented flags:

-file -> "./CW3_FINAL_FINAL.py -file", must have a file input and output entered to solve a grid.

-hints -> "./CW3_FINAL_FINAL.py -hint", enter an N amount of hints for the grids in the script to solve the sudoku. As the number of hints increases the more empty cells are filled. If number of hints exceed the empty cell that grid will be solved.

-explain -> "./CW3_FINAL_FINAL.py -explain", when used it shows where each number should go correspounding to there cell using the grids in the script or a choosen file.

-profile -> "./CW3_FINAL_FINAL.py -profile", with  or without a file(s) input, it produces a plot.

-wavefront -> "./CW3_FINAL_FINAL.py -wavefront", when used it shows the least possible number to be entered in that cell.


Examples of how to use the flags in the Git bash terminal:

"./CW3_FINAL_FINAL.py -file easy1.txt sol_easy1.txt" -> This will solve that inputted grid and saves it into another file as output.

"./CW3_FINAL_FINAL.py -explain" -> This will explain where each number should go for the grids in the script.

"./CW3_FINAL_FINAL.py -file easy1.txt -explain" -> This will explain where each number should go for the grids in the file and outputs a file called "-explain" when opening it shows that expalination.


