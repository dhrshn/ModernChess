import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from pathlib import Path
import time
import chessengine as ChessEngine
from chessengine import GameState, Move

BOARD_WIDTH = BOARD_HEIGHT = 576  
DIMENSION = 9
SQUARE_SIZE = BOARD_HEIGHT // DIMENSION
IMAGES = {}


PIECE_INFO = {
    "P": "President (P):\nMoves one step in any direction (like a standard King).",
    "G": "General (G):\nMoves like a Rook (N, E) and Bishop (NE, NW). Also takes one step South (S).",
    "V": "Vice-General (V):\nMoves like a Rook (S, E, W) and Bishop (SE, SW). Also takes one step North (N).",
    "A": "Air Marshal (A):\nMoves like a Bishop (NE, NW, SE, SW) and also straight North (N).",
    "N": "Navy Seal (N):\nJumps two steps diagonally (NE, NW, SE, SW). Can jump over other pieces.",
    "B": "Army Battalion (B):\nMoves in straight lines (N, S, E, W) like a standard Rook.",
    "S": "Soldier (S):\nMoves like a standard Pawn. One step forward, two on first move. Captures diagonally forward."
}

class ChessUI:
    def __init__(self, root):
        self.root = root
        self.root.title("9x9 Chess Game")
        self.root.configure(bg="#696561")
        
        self.game_state = GameState()
        self.valid_moves = self.game_state.getValidMoves()
        self.state = {"selected": (), "clicks": []}
        self.game_over = False 
        
        self.player_time = 600
        self.opponent_time = 600
        self.timer_running = False
        self.last_time_update = time.time()
        self.move_log = []
        self.move_index = -1
        self.first_move_made = False

        # Main content frame
        main_frame = tk.Frame(root, bg="#696561")
        main_frame.pack(fill="both", expand=True)

        # Create canvas
        self.canvas = tk.Canvas(main_frame, width=BOARD_WIDTH, height=BOARD_HEIGHT)
        self.canvas.pack(side="left", padx=10, pady=10)

        # --- UPDATED: Sidebar now has an info panel ---
        frame_sidebar = tk.Frame(main_frame, bg="#f5dea9", width=250)
        frame_sidebar.pack(side="right", fill="y", padx=10, pady=10)

        # Timer labels
        timer_frame = tk.Frame(frame_sidebar, bg="#f5dea9")
        timer_frame.pack(pady=10)
        self.player_time_label = tk.Label(timer_frame, text="Player Time: 10:00", font=("Arial", 12), bg="#c27421", fg="#f5dea9")
        self.player_time_label.pack(pady=5, padx=10)
        self.opponent_time_label = tk.Label(timer_frame, text="Opponent Time: 10:00", font=("Arial", 12), bg="#c27421", fg="#f5dea9")
        self.opponent_time_label.pack(pady=5, padx=10)

        # Buttons
        button_frame = tk.Frame(frame_sidebar, bg="#f5dea9")
        button_frame.pack(pady=10)
        self.new_game_button = tk.Button(button_frame, text="New Game", command=self.newGame, bg="#c27421", fg="#f5dea9")
        self.new_game_button.pack(pady=5)
        self.undo_button = tk.Button(button_frame, text="Undo", command=self.undoMove, bg="#c27421", fg="#f5dea9")
        self.undo_button.pack(pady=5)
        self.redo_button = tk.Button(button_frame, text="Redo", command=self.redoMove, bg="#c27421", fg="#f5dea9")
        self.redo_button.pack(pady=5)

        #Info Panel
        info_frame = tk.Frame(frame_sidebar, bg="#f5dea9")
        info_frame.pack(pady=10, padx=10, fill="both", expand=True)
        info_title = tk.Label(info_frame, text="Piece Info", font=("Arial", 14, "bold"), bg="#f5dea9")
        info_title.pack(pady=5)
        self.info_text = tk.Text(info_frame, height=10, width=28, wrap="word", font=("Arial", 10), bg="#fcf3d9", relief="sunken", borderwidth=1)
        self.info_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.info_text.insert("1.0", "Click on a piece to see its move description.")
        self.info_text.config(state="disabled")

        # Load images and initialize board
        if self.loadImages():
            self.drawBoard()
            self.drawPieces(self.game_state.board)
            self.canvas.bind("<Button-1>", lambda event: self.onSquareClick(event))
        else:
            self.root.destroy()
            return

    def loadImages(self):
        """
        Load images for the pieces.
        """
        # Note: 'b' images are required for this to run
        pieces = ['wP', 'wG', 'wV', 'wA', 'wN', 'wS', 'wB',
                  'bP', 'bG', 'bV', 'bA', 'bN', 'bS', 'bB']
        try:
            image_path = Path("images") 
            for piece in pieces:
                img_path = image_path / f"{piece}.png"
                if img_path.exists():
                    img = Image.open(img_path)
                    img = img.resize((SQUARE_SIZE, SQUARE_SIZE), Image.Resampling.LANCZOS)
                    IMAGES[piece] = ImageTk.PhotoImage(img)
                else:
                    raise FileNotFoundError(f"Image not found: {img_path}")
        except Exception as e:
            # Added a check for the common case of no 'images' folder
            if isinstance(e, FileNotFoundError):
                 messagebox.showerror("Error", f"Failed to load image: {e.filename}\n\nMake sure you have an 'images' folder in the same directory with all 14 piece PNGs (e.g., wP.png, bP.png).")
            else:
                messagebox.showerror("Error", f"Failed to load chess pieces: {str(e)}")
            return False
        return True

    def drawBoard(self):
        """
        Draw the 9x9 chessboard.
        """
        colors = ["#f0d9b5", "#b58863"]
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                color = colors[(row + col) % 2]
                self.canvas.create_rectangle(
                    col * SQUARE_SIZE, row * SQUARE_SIZE,
                    (col + 1) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE,
                    fill=color, outline=""
                )

    def drawPieces(self, board):
        """
        Draw the pieces on the board.
        """
        self.canvas.delete("pieces")
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                piece = board[row][col]
                if piece != "--" and piece in IMAGES:
                    
                    x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                    y = row * SQUARE_SIZE + SQUARE_SIZE // 2
                    self.canvas.create_image(
                        x, y, image=IMAGES[piece], anchor="c", tags="pieces"
                    )

    def highlightEmptySquares(self, moves):
        """
        Draws dots on valid empty squares.
        This should be called BEFORE drawPieces.
        """
        dot_radius = SQUARE_SIZE // 6
        for move in moves:
            end_row, end_col = move.end_row, move.end_col
            center_x = end_col * SQUARE_SIZE + SQUARE_SIZE // 2
            center_y = end_row * SQUARE_SIZE + SQUARE_SIZE // 2

            self.canvas.create_oval(
                center_x - dot_radius, center_y - dot_radius,
                center_x + dot_radius, center_y + dot_radius,
                fill="#bbbbbb", 
                outline=""
            )

    def highlightCaptureSquares(self, moves):
        """
        Draws rings on valid capture squares.
        This should be called AFTER drawPieces.
        """
        ring_thickness = 3 
        for move in moves:
            end_row, end_col = move.end_row, move.end_col
            self.canvas.create_oval(
                end_col * SQUARE_SIZE + ring_thickness, 
                end_row * SQUARE_SIZE + ring_thickness,
                (end_col + 1) * SQUARE_SIZE - ring_thickness, 
                (end_row + 1) * SQUARE_SIZE - ring_thickness,
                outline="#bbbbbb", 
                width=ring_thickness
            )
            
    #Function to update the info panel
    def updateInfoPanel(self, piece=None):
        """
        Updates the piece info panel with the description of the selected piece.
        """
        self.info_text.config(state="normal")
        self.info_text.delete("1.0", "end")
        if piece and piece != "--":
            piece_type = piece[1]
            description = PIECE_INFO.get(piece_type, "No description available for this piece.")
            self.info_text.insert("1.0", description)
        else:
            self.info_text.insert("1.0", "Click on a piece to see its move description.")
        self.info_text.config(state="disabled")

    def onSquareClick(self, event):
        """
        Handle square clicks.
        """
        
        if self.game_over:
            return

        col = event.x // SQUARE_SIZE
        row = event.y // SQUARE_SIZE
        if not (0 <= row < DIMENSION and 0 <= col < DIMENSION):
            return
        square = (row, col)

        if self.state["selected"]:  # A piece is already selected
            selected_square = self.state["selected"]
            self.state["selected"] = () # Deselect for now
            self.state["clicks"] = []

            if square == selected_square: # Clicked same square
                self.drawBoard()
                self.drawPieces(self.game_state.board)
                self.updateInfoPanel() # Clear info panel
                return # Just deselect, board is cleared of highlights

            # Check if it's a valid move
            move = Move(selected_square, square, self.game_state.board)
            for valid_move in self.valid_moves:
                if move == valid_move:
                    self.game_state.makeMove(valid_move)
                    self.move_log = self.move_log[:self.move_index + 1]
                    self.move_log.append(valid_move)
                    self.move_index += 1
                    if not self.first_move_made:
                        self.first_move_made = True
                        self.startTimer()
                    
                    self.valid_moves = self.game_state.getValidMoves() # Get next player's moves
                    self.drawBoard()
                    self.drawPieces(self.game_state.board)
                    self.updateInfoPanel() # Clear info panel
                    
                    
                    if self.game_state.checkmate:
                        self.game_over = True
                        winner = "Black" if self.game_state.white_to_move else "White"
                        messagebox.showinfo("Game Over", f"Checkmate! {winner} wins.")
                    elif self.game_state.stalemate:
                        self.game_over = True
                        messagebox.showinfo("Game Over", "Stalemate! The game is a draw.")
                        
                    return  # Exit after making a move
        
        # This code runs if no piece was selected, or if an invalid square was clicked
        
        piece = self.game_state.board[row][col]
        
        if piece != "--" and (piece[0] == 'w' if self.game_state.white_to_move else 'b'):
            # This is a valid piece to select
            self.state["selected"] = square
            self.state["clicks"] = [square]
            
            valid_moves = [move for move in self.valid_moves if move.start_row == row and move.start_col == col]
            
            empty_square_moves = [m for m in valid_moves if m.piece_captured == "--"]
            capture_moves = [m for m in valid_moves if m.piece_captured != "--"]

            self.drawBoard()
            self.highlightEmptySquares(empty_square_moves) # Draw dots
            self.drawPieces(self.game_state.board)
            self.highlightCaptureSquares(capture_moves) # Draw rings
            self.updateInfoPanel(piece) # Show info for selected piece
        else:
            # Clicked on an empty square or an enemy piece (with no prior selection)
            self.drawBoard()
            self.drawPieces(self.game_state.board)
            self.updateInfoPanel() # Clear info panel
            # self.state["selected"] is already ()

    def startTimer(self):
        """
        Start the timer.
        """
        if not self.timer_running and not self.game_over:
            self.timer_running = True
            self.last_time_update = time.time()
            self.updateTimer()

    def updateTimer(self):
        """
        Update the timer.
        """
        if self.timer_running and not self.game_over:
            current_time = time.time()
            elapsed_time = current_time - self.last_time_update
            self.last_time_update = current_time
            if self.game_state.white_to_move:
                self.player_time -= elapsed_time
            else:
                self.opponent_time -= elapsed_time
                
            if self.player_time <= 0 or self.opponent_time <= 0:
                self.timer_running = False
                self.game_over = True
                winner = "Black" if self.player_time <= 0 else "White"
                messagebox.showinfo("Game Over", f"Time's up! {winner} wins!")
            else:
                self.player_time_label.config(text=f"Player Time: {int(self.player_time // 60):02d}:{int(self.player_time % 60):02d}")
                self.opponent_time_label.config(text=f"Opponent Time: {int(self.opponent_time // 60):02d}:{int(self.opponent_time % 60):02d}")
                self.root.after(1000, self.updateTimer)

    def newGame(self):
        """
        Start a new game.
        """
        self.game_state = GameState()
        self.valid_moves = self.game_state.getValidMoves()
        self.state = {"selected": (), "clicks": []}
        self.player_time = 600
        self.opponent_time = 600
        self.timer_running = False
        self.last_time_update = time.time()
        self.move_log = []
        self.move_index = -1
        self.first_move_made = False
        self.game_over = False # --- NEW: Reset game over flag ---
        self.drawBoard()
        self.drawPieces(self.game_state.board)
        self.player_time_label.config(text="Player Time: 10:00")
        self.opponent_time_label.config(text="Opponent Time: 10:00")
        self.updateInfoPanel() # Clear info panel

    def undoMove(self):
        """
        Undo the last move.
        """
        if self.move_index >= 0:
            self.game_state.undoMove()
            self.move_index -= 1
            self.valid_moves = self.game_state.getValidMoves()
            self.drawBoard()
            self.drawPieces(self.game_state.board)
            self.updateInfoPanel() # Clear info panel
            self.game_over = False # Game is no longer over
            self.timer_running = self.first_move_made # Resume timer if game had started

    def redoMove(self):
        """
        Redo the last undone move.
        """
        if self.move_index < len(self.move_log) - 1:
            self.move_index += 1
            self.game_state.makeMove(self.move_log[self.move_index]) # makeMove handles checkmate logic
            self.valid_moves = self.game_state.getValidMoves()
            self.drawBoard()
            self.drawPieces(self.game_state.board)
            self.updateInfoPanel() # Clear info panel
            
            # Check for game over state after redoing
            if self.game_state.checkmate:
                self.game_over = True
                winner = "Black" if self.game_state.white_to_move else "White"
                messagebox.showinfo("Game Over", f"Checkmate! {winner} wins.")
            elif self.game_state.stalemate:
                self.game_over = True
                messagebox.showinfo("Game Over", "Stalemate! The game is a draw.")


def main():
    """
    Main function to run the game.
    """
    root = tk.Tk()
    ChessUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
