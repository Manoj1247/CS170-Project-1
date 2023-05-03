class Puzzle:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.operators = ["UP", "DOWN", "LEFT", "RIGHT"]

    def print_puzzle(self, state):
        for i in range(3):
            for j in range(3):
                print(state[3*i + j], end=" ")
            print()

    def get_input(self):
        print("Welcome to XXX 8 puzzle solver.")
        print("Type '1' to use a default puzzle, or '2' to enter your own puzzle.")
        choice = input()
        if choice == '1':
            self.initial_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
            self.goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        elif choice == '2':
            print("Enter your puzzle, use a zero to represent the blank")
            self.initial_state = []
            for i in range(3):
                row = input("Enter the {} row, use space or tabs between numbers: ".format(i+1)).split()
                self.initial_state += [int(num) for num in row]
            print("Enter your choice of algorithm")
            print("1. Uniform Cost Search")
            print("2. A* with the Misplaced Tile heuristic.")
            print("3. A* with the Euclidean distance heuristic.")
            algorithm_choice = input()
            if algorithm_choice == '1':
                print("You chose Uniform Cost Search")
            elif algorithm_choice == '2':
                print("You chose A* with the Misplaced Tile heuristic.")
            elif algorithm_choice == '3':
                print("You chose A* with the Euclidean distance heuristic.")
            else:
                print("Invalid choice. Please try again.")
                self.get_input()
        else:
            print("Invalid choice. Please try again.")
            self.get_input()

    def run(self):
        self.get_input()
        print("Initial state:")
        self.print_puzzle(self.initial_state)
        print("Goal state:")
        self.print_puzzle(self.goal_state)

puzzle = Puzzle([], [])
puzzle.run()
