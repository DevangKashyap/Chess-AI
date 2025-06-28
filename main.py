# Minimax with Alpha-Beta Pruning
import tkinter as tk
from tkinter import messagebox
import copy
import random

# Unicode symbols for chess pieces
PIECE_SYMBOLS = {
    "r": "♜", "n": "♞", "b": "♝", "q": "♛", "k": "♚", "p": "♟",
    "R": "♖", "N": "♘", "B": "♗", "Q": "♕", "K": "♔", "P": "♙"
}

class ChessBoard:
    def __init__(self):
        self.board = [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"]
        ]
        self.turn = "w"  # White moves first

    def is_valid_move(self, start, end):
        return True

    def make_move(self, start, end):
        if self.is_valid_move(start, end):
            self.board[end[0]][end[1]] = self.board[start[0]][start[1]]
            self.board[start[0]][start[1]] = " "
            self.turn = "b" if self.turn == "w" else "w"

    def get_legal_moves(self, color):
        return [((6, 0), (5, 0))]

    def evaluate_board(self):
        return random.randint(-10, 10)

    def minimax(self, depth, alpha, beta, maximizing):
        if depth == 0:
            return self.evaluate_board()
        
        legal_moves = self.get_legal_moves("w" if maximizing else "b")
        
        if maximizing:
            max_eval = float('-inf')
            for move in legal_moves:
                new_board = copy.deepcopy(self)
                new_board.make_move(move[0], move[1])
                eval_score = new_board.minimax(depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                new_board = copy.deepcopy(self)
                new_board.make_move(move[0], move[1])
                eval_score = new_board.minimax(depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval
    
    def get_best_move(self):
        best_move = None
        best_eval = float('-inf')
        
        for move in self.get_legal_moves("b"):
            new_board = copy.deepcopy(self)
            new_board.make_move(move[0], move[1])
            eval_score = new_board.minimax(3, float('-inf'), float('inf'), False)
            if eval_score > best_eval:
                best_eval = eval_score
                best_move = move
        
        return best_move

class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.board = ChessBoard()
        self.buttons = [[None for _ in range(8)] for _ in range(8)]
        self.selected_piece = None
        self.create_board()
    
    def create_board(self):
        for row in range(8):
            for col in range(8):
                frame = tk.Frame(self.root, width=60, height=60)
                frame.grid(row=row, column=col)
                button = tk.Button(frame, font=("Arial", 24), bg="white" if (row + col) % 2 == 0 else "gray",
                                   command=lambda r=row, c=col: self.on_click(r, c))
                button.pack(expand=True, fill=tk.BOTH)
                self.buttons[row][col] = button
        self.update_board()
    
    def on_click(self, row, col):
        if self.selected_piece is None:
            self.selected_piece = (row, col)
        else:
            self.board.make_move(self.selected_piece, (row, col))
            self.selected_piece = None
            self.update_board()
            self.ai_move()
    
    def ai_move(self):
        best_move = self.board.get_best_move()
        if best_move:
            self.board.make_move(best_move[0], best_move[1])
            self.update_board()
    
    def update_board(self):
        for row in range(8):
            for col in range(8):
                piece = self.board.board[row][col]
                self.buttons[row][col].config(text=PIECE_SYMBOLS.get(piece, ""))

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chess AI")
    ChessGUI(root)
    root.mainloop()