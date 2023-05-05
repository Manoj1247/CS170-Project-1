import random


def get_custom_puzzle(puzzle_arr):
    print("Enter your puzzle, use a zero to represent the blank")
    row_name = ["first", "second", "third"]

    for i in range(3):
        while True:
            row_input = input(f"Enter the {row_name[i]} row, use space or tabs between numbers: ")
            row_str_list = row_input.split()
            if len(row_str_list) != 3:
                print("Invalid input! Please enter exactly 3 integers separated by space or tab.")
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
    for row in puzzle_arr:
        print(*row)
    print("")
    

def io_info(puzzle_arr):
    student_id = "862078302"
    print("Welcome to " + student_id + "'s 8 puzzle solver.")

    while True:
        try:
            user_option = int(input("Type \"1\" to use a default puzzle, or \"2\" to enter your own puzzle."))
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


def uniform_cost_search(puzzle_arr):
    print("uniform cost search algo")
    print_puzzle(puzzle_arr)


def a_misplaced_tile(puzzle_arr):
    print("A* with the misplaced tile heuristic")
    print_puzzle(puzzle_arr)


def a_euclidean_distance(puzzle_arr):
    print("A* with the Euclidean distance heuristic")
    print_puzzle(puzzle_arr)


def main():
    puzzle_arr = []
    depth = None
    max_in_queue = None
    num_expanded = None

    algo_choice = io_info(puzzle_arr)
    print_puzzle(puzzle_arr)

    if algo_choice == 1:
        uniform_cost_search(puzzle_arr)
    elif algo_choice == 2:
        a_misplaced_tile(puzzle_arr)
    else:
        a_euclidean_distance(puzzle_arr)

    print("\n\nGoal!!!")
    print(f"\nTo solve this problem the search algorithm expanded a total of {num_expanded} nodes.")
    print(f"The maximum number of nodes in the queue at any one time: {max_in_queue}.")
    print(f"The depth of the goal node was {depth}.")


if __name__ == '__main__':
    main()
