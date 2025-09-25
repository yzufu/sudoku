import random
import time
import os

class SudokuGenerator:
    @staticmethod
    def generate_solved():
        base = 3
        side = base * base

        def pattern(r, c): 
            return (base * (r % base) + r // base + c) % side

        def shuffle(s): 
            return random.sample(s, len(s))
        
        rBase = range(base)
        rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
        cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
        nums = shuffle(range(1, base * base + 1))

        board = [[nums[pattern(r, c)] for c in cols] for r in rows]
        return board

    @staticmethod
    def remove_numbers(board, empty_cells=40):
        board_copy = [row[:] for row in board]
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        
        for i, j in cells[:empty_cells]:
            board_copy[i][j] = 0
            
        return board_copy

class SudokuGame:
    def __init__(self):
        self.generator = SudokuGenerator()
        self.board = []
        self.original = []
        self.solution = []
        self.mistakes = 0
        self.start_time = time.time()
        self.row = 0
        self.col = 0
        self.new_game()
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def new_game(self):
        self.solution = self.generator.generate_solved()
        self.board = self.generator.remove_numbers(self.solution, random.randint(35, 45))
        self.original = [row[:] for row in self.board]
        self.mistakes = 0
        self.start_time = time.time()
        self.row = 0
        self.col = 0
    
    def is_valid_move(self, row, col, num):
        if num == 0:
            return True
            
        for j in range(9):
            if self.board[row][j] == num and j != col:
                return False
        
        for i in range(9):
            if self.board[i][col] == num and i != row:
                return False
        
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == num and (i, j) != (row, col):
                    return False
        
        return True
    
    def display(self):
        self.clear_screen()
        print("=== SUDOKU ===")
        print(f"Time: {int(time.time() - self.start_time)}s | Mistakes: {self.mistakes}")
        print()
        
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("------+-------+------")
            row_str = ""
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    row_str += "| "
                if i == self.row and j == self.col:
                    if self.board[i][j] == 0:
                        row_str += "[ ] "
                    else:
                        row_str += f"[{self.board[i][j]}] "
                else:
                    if self.board[i][j] == 0:
                        row_str += " .  "
                    else:
                        row_str += f" {self.board[i][j]}  "
            print(row_str)
        
        print("\nControls: WASD-move, 1-9-input, 0-clear")
        print("N-new game, C-check, R-solve, Q-quit")
    
    def move_cursor(self, direction):
        if direction == 'w' and self.row > 0:
            self.row -= 1
        elif direction == 's' and self.row < 8:
            self.row += 1
        elif direction == 'a' and self.col > 0:
            self.col -= 1
        elif direction == 'd' and self.col < 8:
            self.col += 1
    
    def input_number(self, num):
        if self.original[self.row][self.col] == 0:
            is_valid = self.is_valid_move(self.row, self.col, num)
            self.board[self.row][self.col] = num
            
            if num != 0 and not is_valid:
                self.mistakes += 1
                return False
            return True
        return False
    
    def check_solution(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return "incomplete"
        
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != self.solution[i][j]:
                    return "wrong"
        return "correct"
    
    def solve(self):
        self.board = [row[:] for row in self.solution]
    
    def run(self):
        while True:
            self.display()
            cmd = input("\nCommand: ").lower()
            
            if cmd == 'q':
                break
            elif cmd == 'n':
                self.new_game()
            elif cmd == 'c':
                result = self.check_solution()
                if result == "correct":
                    print("Correct solution! You win!")
                elif result == "wrong":
                    print("Solution has errors!")
                else:
                    print("Puzzle not complete yet")
                input("Press Enter...")
            elif cmd == 'r':
                self.solve()
            elif cmd in ['w', 'a', 's', 'd']:
                self.move_cursor(cmd)
            elif cmd in '123456789':
                success = self.input_number(int(cmd))
                if not success and cmd != '0':
                    print("Invalid move! Mistake counted.")
                    input("Press Enter...")
            elif cmd == '0':
                self.input_number(0)
            
            result = self.check_solution()
            if result == "correct":
                self.display()
                print("\n*** YOU WIN! ***")
                print(f"Final mistakes: {self.mistakes}")
                input("Press Enter for new game...")
                self.new_game()

if __name__ == "__main__":
    game = SudokuGame()
    game.run()
