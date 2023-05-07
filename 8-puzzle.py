import heapq
import numpy as np
import math
import random


class Node:
    def __init__(self, state, parent=None, action=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = g
        self.h = h
        self.max_queue_size = 0  # Max queue size

    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)


class Puzzle:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.operators = ["UP", "DOWN", "LEFT", "RIGHT"]

    def print_puzzle(self, state):
        puzzle_str = ''
        for i in range(3):
            for j in range(3):
                puzzle_str += str(state[3*i + j]) + ' '
            puzzle_str += '\n'
        return puzzle_str
    
    def random_puzzle(self):
        random_arr = random.sample(range(0, 9), 9)
        arr = []

        for i in range(9):
            arr.append(random_arr.pop(0))

        return arr

    def get_input(self):
        print("Welcome to XXX 8 puzzle solver.")
        print("Type '1' to use a default puzzle, or '2' to enter your own puzzle.")
        choice = input()
        if choice == '1':
            self.initial_state = self.random_puzzle()
            self.goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        elif choice == '2':
            print("Enter your puzzle, use a zero to represent the blank")
            self.initial_state = []
            for i in range(3):
                row = input(
                    "Enter the {} row, use space or tabs between numbers: ".format(i+1)).split()
                self.initial_state += [int(num) for num in row]
            self.goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        print("Enter your choice of algorithm")
        print("1. Uniform Cost Search")
        print("2. A* with the Misplaced Tile heuristic.")
        print("3. A* with the Euclidean distance heuristic.")
        algorithm_choice = input()
        if algorithm_choice == '1':
            print("You chose Uniform Cost Search")
            return 1
        elif algorithm_choice == '2':
            print("You chose A* with the Misplaced Tile heuristic.")
            return 2
        elif algorithm_choice == '3':
            print("You chose A* with the Euclidean distance heuristic.")
            return 3
        else:
            print("Invalid choice. Please try again.")
            self.get_input()

    # function to calculate h value for A* with the

    def find_zero(self, board):
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == 0:
                    return row, col
        return -1, -1

    def uniform_cost_search(self):
        visited = set()
        initial_state = [
            self.initial_state[i * 3:(i + 1) * 3] for i in range(3)]
        tmp_goal_state = [self.goal_state[i * 3:(i + 1) * 3] for i in range(3)]
        priority_queue = [(0, initial_state, [])]
        self.max_queue_size = 1
        nodes_expanded = 0

        while priority_queue:
            numberofmoves, board, path = heapq.heappop(priority_queue)

            if board == tmp_goal_state:
                print("Solution found in {} moves:".format(numberofmoves))
                for move, state in path:
                    print("Move:", move)
                    print(self.print_puzzle([item for sublist in state for item in sublist]))
                print(f"NODES EXPANDED: {nodes_expanded}")
                print(f"MAXIMUM QUEUE SIZE: {self.max_queue_size}")
                return numberofmoves, board

            if str(board) not in visited:
                visited.add(str(board))
                nodes_expanded += 1

                i, j = self.find_zero(board)
                neighbors = [(i-1, j, "UP"), (i+1, j, "DOWN"), (i, j-1, "LEFT"), (i, j+1, "RIGHT")]

                for neighbor in neighbors:
                    row, col, direction = neighbor
                    if row < 0 or row >= len(board) or col < 0 or col >= len(board[row]):
                        continue

                    new_board = [row[:] for row in board]
                    new_board[row][col], new_board[i][j] = new_board[i][j], new_board[row][col]

                    if str(new_board) not in visited:
                        heapq.heappush(
                            priority_queue, (numberofmoves + 1, new_board, path + [(direction, new_board)]))
            
            if len(priority_queue) > self.max_queue_size:
                self.max_queue_size = len(priority_queue)

        return -1, board


    # function to calculate h value for A* with the misplaced tile heuristic
    def h_misplaced(self, state):
        misplaced_tiles = 0
        for i in range(9):
            if state[i] != self.goal_state[i]:
                misplaced_tiles += 1
        return misplaced_tiles

    # function to calculate euclidean distance between 2 points
    def euclidean_distance(self, a, b):
        x1, y1 = a
        x2, y2 = b
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

     # function to calculate h value for A* with the Euclidean distance
    def calculate_h_euclidean(self, state):
        distance = 0
        for i in range(3):
            for j in range(3):
                tile = state[3*i + j]
                if tile != 0:
                    tile_goal_pos = ((tile - 1) // 3, (tile - 1) % 3)
                    tile_curr_pos = (i, j)
                    distance += self.euclidean_distance(
                        tile_goal_pos, tile_curr_pos)
        return distance

    # function to get successors for each state
    def get_child_nodes(self, state):
        # find the blank position
        successors = []
        blank_tile_index = state.index(0)
        blank_tile_row = blank_tile_index//3
        blank_tile_column = blank_tile_index % 3
        for op in self.operators:
            if op == "UP":
                if (blank_tile_row > 0):
                    new_state = state[:]
                    new_state[blank_tile_index], new_state[blank_tile_index -
                                                           3] = new_state[blank_tile_index-3], new_state[blank_tile_index]
                    successors.append((op, new_state))
            elif op == "DOWN":
                if (blank_tile_row < 2):
                    new_state = state[:]
                    new_state[blank_tile_index], new_state[blank_tile_index +
                                                           3] = new_state[blank_tile_index+3], new_state[blank_tile_index]
                    successors.append((op, new_state))
            elif op == "RIGHT":
                if (blank_tile_column < 2):
                    new_state = state[:]
                    new_state[blank_tile_index], new_state[blank_tile_index +
                                                           1] = new_state[blank_tile_index+1], new_state[blank_tile_index]
                    successors.append((op, new_state))
            elif op == "LEFT":
                if (blank_tile_column > 0):
                    new_state = state[:]
                    new_state[blank_tile_index], new_state[blank_tile_index -
                                                           1] = new_state[blank_tile_index-1], new_state[blank_tile_index]
                    successors.append((op, new_state))
        return successors

    def a_star_misplaced(self):
        open_list = []
        self.max_queue_size = 1
        closed_list = set()
        print(open_list)
        start_node = Node(self.initial_state, None, None, 0,
                          self.h_misplaced(self.initial_state))
        heapq.heappush(open_list, start_node)
        while open_list:

            current_node = heapq.heappop(open_list)
            print(
                f'The best state to explore with g={current_node.g} and f={current_node.h} is:\n' f'{self.print_puzzle(current_node.state)}')
            if current_node.state == self.goal_state:
                path = []
                while current_node.parent is not None:
                    path.append(current_node.action)
                    current_node = current_node.parent
                path.reverse()
                print(
                    f'Total number of moves for A* with misplaced : {len(path)}\n')
                print(f'Trace of the path(operators): {path}')
                print(f"NODES EXPANDED = {len(closed_list)}")
                return

            closed_list.add(tuple(current_node.state))

            for action, successor_state in self.get_child_nodes(current_node.state):
                if tuple(successor_state) in closed_list:
                    continue

                g = current_node.g + 1
                h = self.h_misplaced(successor_state)
                successor_node = Node(
                    successor_state, current_node, action, g, h)
                heapq.heappush(open_list, successor_node)
            
            if len(open_list) > self.max_queue_size:
                self.max_queue_size = len(open_list)

        return None

    def a_star_euclidean(self):
        open_list = []
        self.max_queue_size = 1
        closed_list = set()
        start_node = Node(self.initial_state, None, None, 0, 0)
        start_node.h = self.calculate_h_euclidean(self.initial_state)
        heapq.heappush(open_list, start_node)

        # Print initial state of open_list
        print("Initial open_list:", open_list)

        while open_list:
            current_node = heapq.heappop(open_list)
            print(
                f'The best state to explore with g={current_node.g} and f={current_node.h} is:\n' f'{self.print_puzzle(current_node.state)}')
            if current_node.state == self.goal_state:
                path = []
                while current_node.parent is not None:
                    path.append(current_node.action)
                    current_node = current_node.parent
                path.reverse()
                print(
                    f'Total number of moves for A* with Euclidean distance: {len(path)}\n')
                print(f'Trace of the path (operators): {path}')
                print(f"NODES EXPANDED = {len(closed_list)}")
                return

            closed_list.add(tuple(current_node.state))

            for action, successor_state in self.get_child_nodes(current_node.state):
                if tuple(successor_state) in closed_list:
                    continue

                g = current_node.g + 1
                successor_node = Node(successor_state, current_node, action, g)
                successor_node.h = self.calculate_h_euclidean(successor_state)
                heapq.heappush(open_list, successor_node)
            
            if len(open_list) > self.max_queue_size:
                self.max_queue_size = len(open_list)
            
        return None

    def run(self):
        algo = self.get_input()
        if algo == 1:
            moves, goal_state = self.uniform_cost_search()
            print("Solution found in {} moves.".format(moves))
        if (algo == 2):
            self.a_star_misplaced()
        if algo == 3:
            self.a_star_euclidean()

        print("Initial state:")
        print(self.print_puzzle(self.initial_state))
        print("Goal state:")
        print(self.print_puzzle(self.goal_state))
        print("Maximum queue size: {}".format(self.max_queue_size))  # Print maximum queue size


puzzle = Puzzle([], [])
puzzle.run()



