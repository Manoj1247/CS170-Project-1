import random
from queue import PriorityQueue
import math


def get_custom_puzzle(puzzle_arr):
    print("Enter your puzzle, use a zero to represent the blank")
    row_name = ["first", "second", "third"]

    for i in range(3):
        while True:
            row_input = input(
                f"Enter the {row_name[i]} row, use space or tabs between numbers: ")
            row_str_list = row_input.split()
            if len(row_str_list) != 3:
                print(
                    "Invalid input! Please enter exactly 3 integers separated by space or tab.")
            else:
                try:
                    row_int_list = [int(x) for x in row_str_list]
                    puzzle_arr.append(row_int_list)
                    break
                except ValueError:
                    print("Invalid input! Please enter integers only.")


def validate_puzzle(puzzle_arr):
    summation = 0
    for row in puzzle_arr:
        for value in row:
            summation += int(value)

    if summation == 36:
        return True
    else:
        return False


def create_random_puzzle(puzzle_arr):
    random_arr = random.sample(range(0, 9), 9)

    for i in range(3):
        row = []
        for j in range(3):
            row.append(random_arr.pop(0))
        puzzle_arr.append(row)


def print_puzzle(puzzle_arr):
    puzzle_str = ""
    for i in range(len(puzzle_arr)):
        puzzle_str += str(puzzle_arr[i]) + " "
        if (i + 1) % 3 == 0:
            puzzle_str += "\n"
    return puzzle_str


def io_info(puzzle_arr):
    student_id = "XXXXXXXXX"
    print("Welcome to " + student_id + "'s 8 puzzle solver.")

    while True:
        try:
            user_option = int(
                input("Type \"1\" to use a default puzzle, or \"2\" to enter your own puzzle."))
            if user_option == 1 or user_option == 2:
                break
            else:
                print("Invalid input! Please enter 1, 2 or 3")
        except ValueError:
            print("Invalid input! Please enter an integer.")

    if user_option == 1:
        create_random_puzzle(puzzle_arr)
    else:
        get_custom_puzzle(puzzle_arr)
        while not validate_puzzle(puzzle_arr):
            print("PUZZLE NOT VALID. REDO")
            puzzle_arr.clear()
            get_custom_puzzle(puzzle_arr)

    print("\nEnter your choice of algorithm")
    print("Uniform Cost Search")
    print("A* with the Misplaced Tile heuristic.")
    print("A* with the Euclidean distance heuristic.")

    while True:
        try:
            algo_choice = int(input(""))
            if algo_choice == 1 or algo_choice == 2 or algo_choice == 3:
                break
            else:
                print("Invalid input! Please enter 1 or 2")
        except ValueError:
            print("Invalid input! Please enter an integer.")

    return algo_choice


def convert_to_single_array(puzzle_arr):
    temp_arr = []
    for row in puzzle_arr:
        for value in row:
            temp_arr.append(value)

    puzzle_arr.clear()
    for value in temp_arr:
        puzzle_arr.append(value)

# THE ALGORITHMS FOR SEARCH BELOW


class Node:
    def __init__(self, state, parent=None, depth=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.heuristic = self.calculate_heuristic_value()
        if parent:
            self.depth = parent.depth + 1
        else:
            self.depth = 0

    def __lt__(self, other):
        return self.heuristic < other.heuristic

    def calculate_heuristic_value(self):
        total_distance = 0
        for i in range(len(self.state)):
            if self.state[i] == 0:
                continue
            if self.state[i] != i + 1:
                total_distance += 1
        return total_distance


def a_misplaced_tile(puzzle_arr):
    queue = PriorityQueue()
    visited = []
    nodes_expanded = 0
    initial_node = Node(puzzle_arr)
    queue.put((initial_node.heuristic, initial_node))

    while not queue.empty():
        curr_node = queue.get()[1]
        if is_solution(curr_node):
            print("-----SOLUTION FOUND-----")
            print(print_puzzle(curr_node.state))
            return curr_node, nodes_expanded, queue.qsize()
        else:
            print("Expanding State")
            print(print_puzzle(curr_node.state))
            expand(curr_node, queue, visited)
            nodes_expanded += 1

    print("SOLUTION NOT POSSIBLE")
    failure_node = Node([])
    return failure_node, nodes_expanded, queue.qsize()


def a_euclidean_distance(puzzle_arr):
    queue = PriorityQueue()
    visited = []
    nodes_expanded = 0
    initial_node = Node(puzzle_arr)
    queue.put((initial_node.heuristic, initial_node))

    while not queue.empty():
        curr_node = queue.get()[1]
        if is_solution(curr_node):
            print("-----SOLUTION FOUND-----")
            print(print_puzzle(curr_node.state))
            return curr_node, nodes_expanded, queue.qsize()
        else:
            print("Expanding State")
            print(print_puzzle(curr_node.state))
            expand(curr_node, queue, visited)
            nodes_expanded += 1

    print("SOLUTION NOT POSSIBLE")
    failure_node = Node([])
    return failure_node, nodes_expanded, queue.qsize()


def calculate_heuristic_value(node):
    total_distance = 0
    for i in range(len(node.state)):
        if node.state[i] == 0:
            continue
        if node.state[i] != i + 1:
            total_distance += 1
    return total_distance


def is_solution(node):
    solution = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    return solution == node.state


def expand(node, q, visited):

    zero_idx = node.state.index(0)
    n = len(node.state)
    dim = int(n ** 0.5)

# BLANK UP
    if zero_idx - dim >= 0:
        new_node_state = node.state.copy()
        new_node_state[zero_idx], new_node_state[zero_idx -
                                                 3] = new_node_state[zero_idx-3], new_node_state[zero_idx]
        new_node = Node(new_node_state, parent=node)
        if new_node_state not in visited:
            visited.append(new_node_state)
            q.put((calculate_heuristic_value(new_node), new_node))

# BLANK DOWN
    if zero_idx + dim < n:
        new_node_state = node.state.copy()
        new_node_state[zero_idx], new_node_state[zero_idx +
                                                 3] = new_node_state[zero_idx+3], new_node_state[zero_idx]
        new_node = Node(new_node_state, parent=node)
        if new_node_state not in visited:
            visited.append(new_node_state)
            q.put((calculate_heuristic_value(new_node), new_node))

# BLANK LEFT
    if zero_idx % dim != 0:
        new_node_state = node.state.copy()
        new_node_state[zero_idx], new_node_state[zero_idx -
                                                 1] = new_node_state[zero_idx-1], new_node_state[zero_idx]
        new_node = Node(new_node_state, parent=node)
        if new_node_state not in visited:
            visited.append(new_node_state)
            q.put((calculate_heuristic_value(new_node), new_node))

# BLANK RIGHT
    if (zero_idx + 1) % dim != 0:
        new_node_state = node.state.copy()
        new_node_state[zero_idx], new_node_state[zero_idx +
                                                 1] = new_node_state[zero_idx + 1], new_node_state[zero_idx]
        new_node = Node(new_node_state, parent=node)
        if new_node_state not in visited:
            visited.append(new_node_state)
            q.put((calculate_heuristic_value(new_node), new_node))


def main():
    puzzle_arr = []
    depth = None
    max_in_queue = None
    num_expanded = None

    algo_choice = io_info(puzzle_arr)
    convert_to_single_array(puzzle_arr)

    if algo_choice == 1:
        print("UNIFORM COST")
    elif algo_choice == 2:
        finished_node, num_expanded, max_in_queue = a_misplaced_tile(
            puzzle_arr)
        if len(finished_node.state) > 0:
            depth = finished_node.depth
    else:
        finished_node, num_expanded, max_in_queue = a_euclidean_distance(
            puzzle_arr)
        if len(finished_node.state) > 0:
            depth = finished_node.depth

    print("\n\nGoal!!!")
    print(
        f"\nTo solve this problem the search algorithm expanded a total of {num_expanded} nodes.")
    print(
        f"The maximum number of nodes in the queue at any one time: {max_in_queue}.")
    print(f"The depth of the goal node was {depth}.")


if __name__ == '__main__':
    main()
