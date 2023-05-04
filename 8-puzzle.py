import heapq
class Node:
    def __init__(self, state, parent=None, action=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = g
        self.h = h

    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)
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
            self.initial_state = [1, 2, 3, 4, 5, 0, 6, 7, 8]
            self.goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        elif choice == '2':
            print("Enter your puzzle, use a zero to represent the blank")
            self.initial_state = []
            for i in range(3):
                row = input("Enter the {} row, use space or tabs between numbers: ".format(i+1)).split()
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
 
    #function to calculate h value for A* with the misplaced tile heuristic 
    def h_misplaced(self, state):
        misplaced_tiles = 0
        for i in range(9):
            if state[i] != self.goal_state[i]:
                misplaced_tiles += 1
        return misplaced_tiles
    #function to get successors for each state    
    def get_child_nodes(self, state):
        #find the blank position
        successors = []
        blank_tile_index = state.index(0)
        blank_tile_row = blank_tile_index//3 
        blank_tile_column = blank_tile_index%3 
        for op in self.operators:
          if op == "UP":
            if(blank_tile_row>0):  
              new_state = state[:]
              new_state[blank_tile_index], new_state[blank_tile_index-3] = new_state[blank_tile_index-3], new_state[blank_tile_index]
              successors.append((op, new_state))
          elif op == "DOWN":
              if(blank_tile_row<2):
                  new_state = state[:]
                  new_state[blank_tile_index], new_state[blank_tile_index+3] = new_state[blank_tile_index+3], new_state[blank_tile_index]
                  successors.append((op, new_state))
          elif op == "RIGHT":
                if(blank_tile_column<2):
                  new_state = state[:]
                  new_state[blank_tile_index], new_state[blank_tile_index+1] = new_state[blank_tile_index+1], new_state[blank_tile_index]
                  successors.append((op, new_state))
          elif op == "LEFT":
                if(blank_tile_column>0):
                    new_state = state[:]
                    new_state[blank_tile_index], new_state[blank_tile_index-1] = new_state[blank_tile_index-1], new_state[blank_tile_index]
                    successors.append((op, new_state))
        return successors
    
    def a_star_misplaced(self):
        open_list = []
        closed_list = set()
        print(open_list)
        start_node = Node(self.initial_state, None, None, 0, self.h_misplaced(self.initial_state) )
        heapq.heappush(open_list, start_node)
        while open_list:
            
            current_node = heapq.heappop(open_list)
            print(current_node.state, 'current') 
            if current_node.state == self.goal_state:
                path = []
                while current_node.parent is not None:
                    path.append(current_node.action)
                    current_node = current_node.parent
                path.reverse()
                return path

            closed_list.add(tuple(current_node.state))

            for action, successor_state in self.get_child_nodes(current_node.state):
                if tuple(successor_state) in closed_list:
                    continue

                g = current_node.g + 1
                h = self.h_misplaced(successor_state)
                successor_node = Node(successor_state, current_node, action, g, h)
                heapq.heappush(open_list, successor_node)

        return None

    def run(self):
        algo = self.get_input()
        if(algo==2):
          print (self.a_star_misplaced())
        print("Initial state:")
        self.print_puzzle(self.initial_state)
        print("Goal state:")
        self.print_puzzle(self.goal_state)

puzzle = Puzzle([], [])
puzzle.run()
