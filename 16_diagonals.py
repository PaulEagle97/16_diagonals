"""
This script contains a backtracking algorithm for solving the 16-diagonal puzzle.
The goal in this puzzle is to place diagonals inside cells of a square grid 
such that no two diagonals have a common point, or in other words, 
they do not touch each other.
"""
import copy
import time

def get_valid_moves(board_state, board_size):
    """
    A helper function which calculates all legal moves
    for the next cell, taking other cell values into consideration.
    
    Input: Current state of the board, board size
    Output: A sorted list with all valid values
    """
    valid_moves = {0, 1, 2}
    invalid_moves = set()
    # current column idx
    col = len(board_state[-1])
    # a dictionary with values that each move cancels in nearby cells
    pos_dict = {1:{'down-left':1, 'down':2, 'down-right':None, 'right':2},
                2:{'down-left':None, 'down':1, 'down-right':2, 'right':1},
                0:{'down-left':None, 'down':None, 'down-right':None, 'right':None}}
    # check the upper cell
    cell_val = board_state[-2][col]
    invalid_moves.add(pos_dict[cell_val]['down'])

    if col > 0:
        # check the uppper-left cell
        cell_val = board_state[-2][col-1]
        invalid_moves.add(pos_dict[cell_val]['down-right'])
        # check the left cell
        cell_val = board_state[-1][col-1]
        invalid_moves.add(pos_dict[cell_val]['right'])
    if col < board_size - 1:
        # check the upper-right cell
        cell_val = board_state[-2][col+1]
        invalid_moves.add(pos_dict[cell_val]['down-left'])

    # substract invalid moves from all possible moves
    valid_moves.difference_update(invalid_moves)
    # return valid values in descending order
    # ('0' to be considered the last)
    return sorted(list(valid_moves), reverse=True)


def recursive_fast (curr_state, n):
    """
    A recursive algorithm, that solves the puzzle of the given grid size
    by placing <n> number of diagonals inside the grid without breaking the rules.
    Returns the first encountered solution.

    Input: initialized grid of the form = [[0, 0, ... 0][]] and the desired number of diagonals
    Output: a filled-out grid if any solution is found or <None> otherwise
    """
    diag_vals = [1, 2]
    board_size = len(curr_state[-2])
    num_total_cells = board_size ** 2 + board_size
    num_filled_cells = sum(len(row) for row in curr_state)
    num_diags = sum(row.count(val) for row in curr_state for val in diag_vals)

    # BASE CASE
    # check if the desired number of diagonals is already placed
    if num_diags == n:
        return curr_state[1:]
    # check if the number of missing diagonals 
    # is greater than the number of available cells
    elif (n - num_diags) > (num_total_cells - num_filled_cells):
        return None
    
    # calculate all valid moves for the next step
    valid_moves = get_valid_moves(curr_state[-2:], board_size)

    # iterate through every move
    for move in valid_moves:
        # add the move to the current board state
        next_state = copy.deepcopy(curr_state)
        next_state[-1].append(move)
        # check if the current row is full
        if len(next_state[-1]) == board_size:
            # initialize a new row
            next_state.append([])

        # call an instance of the function with updated state
        solution = recursive_fast(next_state, n)
        
        # if any solution is found, return it
        if solution != None:
            return solution
        
    # no solutions are found
    return None


def main():

    num_diags = 16
    board_size = 5
    init_lst = []
    grid_dict = {0:' ', 1:'/', 2:'\\'}
    for _ in range(board_size):
        init_lst.append(0)

    start_time = time.time()
    recurs_sol = recursive_fast([init_lst, []], num_diags)
    elapsed_time = time.time() - start_time
    print ('Time elapsed:', elapsed_time)

    if recurs_sol != None:
        print("Solution:")
        for row in recurs_sol:
            if len(row) > 0:
                str_row = ''
                for elem in row:
                    str_row += ('|' + f'{grid_dict[elem]}')
                str_row += '|'
                print (str_row)
    else:
        print ('There are no solutions.')


if __name__ == "__main__":
    print('<<< SCRIPT START >>>\n')
    main()
    print('\n<<< SCRIPT END >>>\n')