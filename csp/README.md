# **Kakuro Puzzle**
This section of the project deals with the solution of the [Kakuro Puzzle](https://en.wikipedia.org/wiki/Kakuro) as a constraint satisfaction problem (CSP). The constraint propogation technique used in this problem is **Arc consistency-3** (or AC3 for short), hence implemented by the **Maintaining Arc Consistency** as well as the **Backtracking search** algorithms.

- **'testcases/'** - the sub-directory that contains all the sample test inputs that takes the form of an incomplete Kakuro puzzle.
- **.py files** - Python files containing the main part of the code.
- **Makefile** - for ease of access of running and demonstration.

> ***NOTE***: A sub-directory **'outputs/'** will be created when the Makefile is executed. This folder contains the corresponding solved outputs of the sample inputs of the project.

## How to run?
- In the terminal, execute the command:
    ```
    make run
    ```
    This will automatically create the output folders, and create the output files of the corresponding input testcases after running the program by calling the input.py file.  
    The output files will be the solved Kakuro input puzzles.  
    Do make clean to remove the temporary files after use.
    ```
    make clean
    ```

