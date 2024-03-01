from queue import PriorityQueue
from random import shuffle


class PuzzleNode:
    def __init__(self, puzzle, parent=None, move=None):
        self.puzzle = puzzle
        self.parent = parent
        self.move = move
        if parent:
            self.g = parent.g + 1
        else:
            self.g = 0
        self.h = self.calculate_heuristic()
        self.f = self.g + self.h

    def __lt__(self, other):
        return self.f < other.f

    def generate_children(self):
        children = []
        blank_row, blank_col = self.get_blank_position()
        possible_moves = self.get_possible_moves()
        for move, (row, col) in possible_moves:
            new_puzzle = [list(row) for row in self.puzzle]
            new_puzzle[row][col], new_puzzle[blank_row][blank_col] = new_puzzle[blank_row][blank_col], new_puzzle[row][
                col]
            children.append(PuzzleNode(new_puzzle, parent=self, move=move))
        return children

    def calculate_heuristic(self):
        total_distance = 0
        for i in range(3):
            for j in range(3):
                if self.puzzle[i][j] != 0:
                    goal_row, goal_col = divmod(self.puzzle[i][j] - 1, 3)
                    total_distance += abs(i - goal_row) + abs(j - goal_col)
        return total_distance

    def get_blank_position(self):
        for i in range(3):
            for j in range(3):
                if self.puzzle[i][j] == 0:
                    return i, j

    def get_possible_moves(self):
        moves = []
        blank_row, blank_col = self.get_blank_position()
        if blank_row > 0:
            moves.append(('UP', (blank_row - 1, blank_col)))
        if blank_row < 2:
            moves.append(('DOWN', (blank_row + 1, blank_col)))
        if blank_col > 0:
            moves.append(('LEFT', (blank_row, blank_col - 1)))
        if blank_col < 2:
            moves.append(('RIGHT', (blank_row, blank_col + 1)))
        return moves


def generate_random_state():
    numbers = list(range(9))
    shuffle(numbers)
    state = [numbers[i:i + 3] for i in range(0, 9, 3)]
    return state


def is_solvable(initialstate, goalstate):
    inversion_count = 0
    initialpositionstate = [item for sublist in initialstate for item in sublist]
    goalpositionstate = [item for sublist in goalstate for item in sublist]
    vec = [item for sublist in goalstate for item in sublist]
    for i in range(9):
        for j in range(9):
            if initialpositionstate[i] == goalpositionstate[j]:
                if j == 0:
                    vec[i] = 9
                else:
                    vec[i] = j

    for i in range(9):
        for j in range(i + 1, 9):
            if vec[i] > vec[j]:
                inversion_count += 1

    return inversion_count % 2 == 0


def solve_8_puzzle():
    initial_state = generate_random_state()
    goal_state = generate_random_state()

    while not is_solvable(initial_state, goal_state):
        initial_state = generate_random_state()
        goal_state = generate_random_state()

    print("Initial State:")
    for row in initial_state:
        print(row)

    print("\nGoal State:")
    for row in goal_state:
        print(row)

    initial_node = PuzzleNode(initial_state)
    frontier = PriorityQueue()
    frontier.put(initial_node)

    visited = set()

    while not frontier.empty():
        current_node = frontier.get()
        if current_node.puzzle == goal_state:
            moves = []
            while current_node.parent:
                moves.append((current_node.move, current_node.puzzle))
                current_node = current_node.parent
            moves.reverse()
            for move, puzzle in moves:
                print(f"\nMove: {move}")
                for row in puzzle:
                    print(row)
            return

        visited.add(tuple(map(tuple, current_node.puzzle)))

        children = current_node.generate_children()
        for child in children:
            if tuple(map(tuple, child.puzzle)) not in visited:
                frontier.put(child)


solve_8_puzzle()
