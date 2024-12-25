import heapq

class BlockedNQueens:
    def __init__(self, n, blocked_cells, heuristic_choice="h1"):
        self.n = n
        self.blocked_cells = set(blocked_cells)
        self.heuristic_choice = heuristic_choice

    def is_valid(self, state, row, col):
        for r, c in state:
            if c == col or r + c == row + col or r - c == row - col:
                return False
        return (row, col) not in self.blocked_cells

    def heuristic_h1(self, state):
        #Heuristic 1: Remaining queens multiplied by the minimal free cells
        attacked_cells = set()
        for r, c in state:
            for i in range(self.n):
                attacked_cells.add((r, i))
                attacked_cells.add((i, c))
                attacked_cells.add((r + i, c + i))
                attacked_cells.add((r - i, c - i))
                attacked_cells.add((r + i, c - i))
                attacked_cells.add((r - i, c + i))

        free_cells = set((r, c) for r in range(self.n) for c in range(self.n))
        free_cells -= attacked_cells
        free_cells -= self.blocked_cells

        queens_left = self.n - len(state)
        return queens_left * len(free_cells)

    def heuristic_h2(self, state):
        #Heuristic 2: Sum of minimum distances for remaining queens
        queens_left = self.n - len(state)
        if not state:
            return 0
        distances = []
        for row in range(len(state), self.n):
            min_distance = float('inf')
            for col in range(self.n):
                if self.is_valid(state, row, col):
                    distance = min(abs(row - r) + abs(col - c) for r, c in state)
                    min_distance = min(min_distance, distance)
            if min_distance != float('inf'):
                distances.append(min_distance)
        return sum(distances)

    def heuristic_h3(self, state):
        #Heuristic 3: Number of queens in conflict
        conflicts = 0
        for i, (r1, c1) in enumerate(state):
            for r2, c2 in state[i + 1:]:
                if c1 == c2 or r1 + c1 == r2 + c2 or r1 - c1 == r2 - c2:
                    conflicts += 1
        return conflicts

    def heuristic(self, state):
        if self.heuristic_choice == "h1":
            return self.heuristic_h1(state)
        elif self.heuristic_choice == "h2":
            return self.heuristic_h2(state)
        elif self.heuristic_choice == "h3":
            return self.heuristic_h3(state)
        else:
            raise ValueError("Invalid heuristic choice!")

    def generate_neighbors(self, state):
        row = len(state)
        neighbors = []
        for col in range(self.n):
            if self.is_valid(state, row, col):
                neighbors.append(state + [(row, col)])
        return neighbors

    def solve(self):
        #A* algorithm
        open_set = []
        heapq.heappush(open_set, (0, [], 0))  # (priority, state, cost_so_far)

        while open_set:
            _, current_state, g = heapq.heappop(open_set)

            if len(current_state) == self.n:
                return current_state

            for neighbor in self.generate_neighbors(current_state):
                cost = g + 1
                priority = cost + self.heuristic(neighbor)
                heapq.heappush(open_set, (priority, neighbor, cost))

        return None

    def is_admissible(self):
        admissible = True
        print("\nChecking heuristic admissibility:")
        for state in self.generate_test_states():
            true_cost = self.calculate_true_cost(state)
            heuristic_value = self.heuristic(state)
            print(f"State: {state}, h(n)={heuristic_value}, g*(n)={true_cost}")
            if heuristic_value > true_cost:
                print(f"-> Not admissible for state {state}: h(n)={heuristic_value}, g*(n)={true_cost}")
                admissible = False
        return admissible

    def generate_test_states(self):
        return [
            [],
            [(0, 0)],
            [(0, 0), (1, 2)],
        ]

    def calculate_true_cost(self, state):
        return self.n - len(state)

def main():
    n = 8
    blocked_cells = [(0, 1), (3, 5), (4, 2)]

    for heuristic in ["h1", "h2", "h3"]:
        print(f"\nTesting heuristic: {heuristic}")
        solver = BlockedNQueens(n, blocked_cells, heuristic_choice=heuristic)


        admissible = solver.is_admissible()
        if admissible:
            print("The heuristic is admissible!")
        else:
            print("The heuristic is NOT admissible.")


        solution = solver.solve()
        if solution:
            print("Solution found:")
            for row, col in solution:
                print(f"Queen at row {row}, column {col}")
        else:
            print("No solution exists for this problem.")

if __name__ == "__main__":
    main()
