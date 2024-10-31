import tkinter as tk
import random

class XOGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic-Tac-Toe Almdrasa")

        self.player_score = 0
        self.computer_score = 0
        
        self.board = [" " for _ in range(9)]
        self.current_player = "X"
        self.history = []  # To track moves for undo functionality
        
        self.buttons = [tk.Button(master, text=" ", font='Arial 20', width=5, height=2, 
                                   command=lambda i=i: self.player_move(i)) for i in range(9)]

        self.score_label = tk.Label(master, text=f"Player: {self.player_score}  Computer: {self.computer_score}", font='Arial 16')
        self.score_label.grid(row=0, column=0, columnspan=3)

        self.status_label = tk.Label(master, text="", font='Arial 16')
        self.status_label.grid(row=1, column=0, columnspan=3)

        self.reset_button = tk.Button(master, text="Restart Game", command=self.reset_game)
        self.reset_button.grid(row=2, column=0, columnspan=3, sticky="ew")

        self.undo_button = tk.Button(master, text="Undo", command=self.undo_move, state=tk.DISABLED)
        self.undo_button.grid(row=3, column=0, columnspan=3, sticky="ew")

        for i, button in enumerate(self.buttons):
            button.grid(row=(i // 3) + 4, column=i % 3)

    def player_move(self, index):
        if self.board[index] == " ":
            self.board[index] = self.current_player
            self.history.append(index)  # Save the move to history
            self.buttons[index].config(text=self.current_player)
            self.undo_button.config(state=tk.NORMAL)  # Enable undo button
            if self.check_winner(self.current_player):
                self.player_score += 1
                self.update_score()
                self.status_label.config(text="You Win!")
                self.highlight_winner(self.current_player)
            elif " " not in self.board:
                self.status_label.config(text="It's a Tie!")
                self.highlight_tie()
            else:
                self.current_player = "O"
                self.computer_move()

    def computer_move(self):
        available_moves = [i for i in range(9) if self.board[i] == " "]
        if available_moves:
            index = random.choice(available_moves)
            self.board[index] = self.current_player
            self.history.append(index)  # Save the computer's move to history
            self.buttons[index].config(text=self.current_player)
            self.undo_button.config(state=tk.NORMAL)  # Enable undo button
            if self.check_winner(self.current_player):
                self.computer_score += 1
                self.update_score()
                self.status_label.config(text="Computer Wins!")
                self.highlight_winner(self.current_player)
            elif " " not in self.board:
                self.status_label.config(text="It's a Tie!")
                self.highlight_tie()
            else:
                self.current_player = "X"

    def undo_move(self):
        if self.history:
            last_move = self.history.pop()  # Get the last move
            self.board[last_move] = " "  # Clear that cell
            self.buttons[last_move].config(text=" ", bg='SystemButtonFace')  # Reset button
            self.current_player = "X" if self.current_player == "O" else "O"  # Switch players
            self.status_label.config(text="")  # Clear status message

            # Disable undo button if no more moves to undo
            if not self.history:
                self.undo_button.config(state=tk.DISABLED)

    def check_winner(self, player):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        return any(all(self.board[i] == player for i in condition) for condition in win_conditions)

    def update_score(self):
        self.score_label.config(text=f"Player: {self.player_score}  Computer: {self.computer_score}")

    def reset_board(self):
        for i in range(9):
            self.board[i] = " "
            self.buttons[i].config(text=" ", bg='SystemButtonFace', state=tk.NORMAL)
        self.current_player = "X"
        self.status_label.config(text="")
        self.history.clear()  # Clear history for the new game
        self.undo_button.config(state=tk.DISABLED)  # Disable undo button

    def reset_game(self):
        self.player_score = 0
        self.computer_score = 0
        self.update_score()
        self.reset_board()

    def highlight_winner(self, winner):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        for condition in win_conditions:
            if all(self.board[i] == winner for i in condition):
                for i in condition:
                    self.buttons[i].config(bg='cyan')  # Highlight winning cells in cyan
                self.disable_buttons()
                break  # Stop after highlighting the first winning condition

    def highlight_tie(self):
        for button in self.buttons:
            button.config(bg='red')  # Highlight all cells in red for a tie
        self.disable_buttons()

    def disable_buttons(self):
        for button in self.buttons:
            button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    game = XOGame(root)
    root.mainloop()
