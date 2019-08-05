'''
Marble solitaire (or peg solitaire, but marbles are cooler) is a game played with a board containing 33 slots and 32 marbles. I can remove marbles from the board by jumping over them with another marble. The goal is to remove every marble except one from the board.

This all started when my sister *claimed* that she solved the game. I, too, wanted to solve the game, but I was too lazy to keep trying by hand and not enough of a genius to just go ahead and solve the whole thing in my head, I wrote this script.

Using a recursive function, this script generates all possible board states all the way down from starting with a full board to having no more moves left. It then lets you select a winning board state and follow that all the way back up to figure out which moves you need to make to end up with that board state.
'''



import numpy as np
import pandas as pd


# This is what my starting board should look like
'''
x x x x x x x x x x x
x x x x x x x x x x x
x x x x 1 1 1 x x x x
x x x x 1 1 1 x x x x
x x 1 1 1 1 1 1 1 x x
x x 1 1 1 -1 1 1 1 x x
x x 1 1 1 1 1 1 1 x x
x x x x 1 1 1 x x x x
x x x x 1 1 1 x x x x
x x x x x x x x x x x
x x x x x x x x x x x
'''

# Setting up the starting board
starting_board = pd.DataFrame([[0 for x in range(11)] for y in range(11)])

starting_board.iloc[2,4:7] = 1
starting_board.iloc[3,4:7] = 1
starting_board.iloc[4,2:9] = 1
starting_board.iloc[5,2:9] = 1
starting_board.iloc[6,2:9] = 1
starting_board.iloc[7,4:7] = 1
starting_board.iloc[8,4:7] = 1

starting_board.iloc[5,5] = -1

starting_board

# Setting up basic tree class that can have children and parents. That way I can trace the moves I took to get to a certain board state.
class Tree:
    def __init__(self, board):
        self.board = board
        self.children = []

    def add_child(self, board):
        newchild = Tree(board)
        newchild.parent = self
        self.children.append(newchild)
        return newchild

# Setting up global variables for the function to write to. These are what I'll later call to check generated boards.
counter = 0
boards = []
final_boards = []

# Define the make_moves function. This recursive function takes a member of the Tree class, calls the board of that Tree, and then for each position in that board checks of there are any possible moves. If there are, it makes that move, generates the new board, appens the new board to a global list, and calls itself on the newly generated board. If there are no possible moves and there is only one marble left in the middle of the board, the game is won, and the board stateis appended to final_boards.
def make_moves(tree):
    starting_board = tree.board
    global counter
    if counter % 1000 == 0:
        print(counter)
        print('boards:', len(boards))
        print('success boards:', len(final_boards))
    for col in range(11):
        for row in range(11):
            if starting_board.iloc[row, col] == 1:
                if starting_board.iloc[row+2, col] == -1 and starting_board.iloc[row+1, col] == 1:
                    new_board = starting_board.copy()
                    new_board.iloc[row+2, col] = 1
                    new_board.iloc[row+1, col] = -1
                    new_board.iloc[row, col] = -1
                    boards.append(tree.add_child(new_board))
                    counter += 1
                    make_moves(tree.add_child(new_board))
                if starting_board.iloc[row-2, col] == -1 and starting_board.iloc[row-1, col] == 1:
                    new_board = starting_board.copy()
                    new_board.iloc[row-2, col] = 1
                    new_board.iloc[row-1, col] = -1
                    new_board.iloc[row, col] = -1
                    boards.append(tree.add_child(new_board))
                    counter += 1
                    make_moves(tree.add_child(new_board))
                if starting_board.iloc[row, col+2] == -1 and starting_board.iloc[row, col+1] == 1:
                    new_board = starting_board.copy()
                    new_board.iloc[row, col+2] = 1
                    new_board.iloc[row, col+1] = -1
                    new_board.iloc[row, col] = -1
                    boards.append(tree.add_child(new_board))
                    counter += 1
                    make_moves(tree.add_child(new_board))
                if starting_board.iloc[row, col-2] == -1 and starting_board.iloc[row, col-1] == 1:
                    new_board = starting_board.copy()
                    new_board.iloc[row, col-2] = 1
                    new_board.iloc[row, col-1] = -1
                    new_board.iloc[row, col] = -1
                    boards.append(tree.add_child(new_board))
                    counter += 1
                    make_moves(tree.add_child(new_board))
            elif starting_board.sum().sum() == -31 and starting_board.iloc[5,5] == 1:
                    final_boards.append(starting_board)
                    return tree
            else:
                continue

# Generate final boards
make_moves(Tree(starting_board))

# Define helper function to display an entire branch of a tree, from a node up
def show_branch(node):
    try:
        print(node.parent.board)
        show_branch(node.parent)
    except:
        print(node.board)

# Run that helper function on one of the success boards
show_branch(final_boards[1])
