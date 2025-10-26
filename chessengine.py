class GameState:
    def __init__(self):
        """
        Board is a 9x9 2D list. Each element has 2 characters.
        The first character represents the color: 'w' or 'b'.
        The second character represents the piece type.
        "--" represents an empty square.
        """
        self.board = [
            ["bA", "bN", "bV", "bB", "bP", "bG", "bV", "bN", "bA"],
            ["bS", "bS", "bS", "bS", "bS", "bS", "bS", "bS", "bS"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["wS", "wS", "wS", "wS", "wS", "wS", "wS", "wS", "wS"],
            ["wA", "wN", "wV", "wB", "wP", "wG", "wV", "wN", "wA"]
        ]
        self.moveFunctions = {
            "P": self.getPresidentMoves,
            "G": self.getGeneralMoves,
            "V": self.getViceGeneralMoves,
            "A": self.getAirMarshalMoves,
            "N": self.getNavySealMoves,
            "S": self.getSoldierMoves,
            "B": self.getArmyBattalionMoves 
        }
        self.white_to_move = True
        self.move_log = []
        
        self.white_president_location = (8, 4)
        self.black_president_location = (0, 4)
        
        # --- ADDED checkmate flag ---
        self.checkmate = False
        # --- Stalemate flag is NOT added, as requested ---

    def makeMove(self, move):
        """
        Execute a move. (This is NOT for check validation)
        """
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
        
        # Update president location
        if move.piece_moved == "wP":
            self.white_president_location = (move.end_row, move.end_col)
        elif move.piece_moved == "bP":
            self.black_president_location = (move.end_row, move.end_col)

        # --- BUGFIX: REMOVED all checkmate logic from makeMove ---
        # The UI (chessui.py) is responsible for calling getValidMoves
        # and checking for checkmate *after* this function returns.
        # Calling it here was causing a state bug.
        
    def undoMove(self):
        """
        Undo the last move.
        """
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move
            
            # Update president location
            if move.piece_moved == "wP":
                self.white_president_location = (move.start_row, move.start_col)
            elif move.piece_moved == "bP":
                self.black_president_location = (move.start_row, move.start_col)
                
            # --- RESET checkmate flag on undo ---
            self.checkmate = False

    # --- ADDED inCheck() function ---
    def inCheck(self):
        """
        Determine if the current player is in check.
        """
        if self.white_to_move:
            return self.squareUnderAttack(self.white_president_location[0], self.white_president_location[1])
        else:
            return self.squareUnderAttack(self.black_president_location[0], self.black_president_location[1])

    # --- ADDED squareUnderAttack() function ---
    def squareUnderAttack(self, row, col):
        """
        Determine if the square (row, col) is under attack by the opponent.
        """
        # --- BUGFIX: REMOVED state-flipping ---
        # Get opponent moves without changing the game's state
        opponent_moves = self._getAllPossibleMovesUnchecked(not self.white_to_move)
        # --- BUGFIX: REMOVED state-flipping ---
        
        for move in opponent_moves:
            if move.end_row == row and move.end_col == col:
                return True
        return False

    def getValidMoves(self):
        """
        Get all valid moves considering checks.
        """
        # --- REVERTED to the complex logic ---
        # --- BUGFIX: Pass the current turn state ---
        moves = self._getAllPossibleMovesUnchecked(self.white_to_move) # Get all moves
        
        # For each move, make the move, check if it's valid (not in check), then undo
        for i in range(len(moves) - 1, -1, -1): # Iterate backwards
            move = moves[i]
            
            # Simulate the move
            self.board[move.start_row][move.start_col] = "--"
            self.board[move.end_row][move.end_col] = move.piece_moved
            
            # Store old president location if it moved
            old_president_loc = None
            if move.piece_moved == "wP":
                old_president_loc = self.white_president_location
                self.white_president_location = (move.end_row, move.end_col)
            elif move.piece_moved == "bP":
                old_president_loc = self.black_president_location
                self.black_president_location = (move.end_row, move.end_col)

            # Check if the current player is now in check
            if self.inCheck(): 
                moves.remove(move) # If it's in check, it's not a valid move

            # Undo the simulated move
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            
            # Restore president location
            if move.piece_moved == "wP":
                self.white_president_location = old_president_loc
            elif move.piece_moved == "bP":
                self.black_president_location = old_president_loc
                
        return moves

    def _getAllPossibleMovesUnchecked(self, is_white_turn):
        """
        Get all possible moves without considering checks.
        Takes a parameter to know whose moves to get,
        so it doesn't rely on (or change) the main game state.
        """
        moves = []
        for row in range(9):
            for col in range(9):
                piece = self.board[row][col]
                # --- BUGFIX: Use the 'is_white_turn' parameter ---
                if piece != "--" and (piece[0] == 'w' if is_white_turn else 'b'):
                    self.moveFunctions[piece[1]](row, col, moves)
        return moves

    def getPresidentMoves(self, row, col, moves):
        """
        President moves one step in any direction.
        (Logic is correct, prevents friendly fire)
        """
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for d in directions:
            end_row = row + d[0]
            end_col = col + d[1]
            if 0 <= end_row < 9 and 0 <= end_col < 9:
                end_piece = self.board[end_row][end_col]
                # This line correctly prevents capturing friendly pieces
                if end_piece == "--" or end_piece[0] != self.board[row][col][0]:
                    moves.append(Move((row, col), (end_row, end_col), self.board))

    def getGeneralMoves(self, row, col, moves):
        """
        General moves: N, NE, NW, E, and one step S.
        (Logic is correct, prevents friendly fire)
        """
        directions = [(-1, 0), (-1, 1), (-1, -1), (0, 1)]
        for d in directions:
            for i in range(1, 9):
                end_row = row + d[0] * i
                end_col = col + d[1] * i
                if 0 <= end_row < 9 and 0 <= end_col < 9:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    # This line correctly prevents capturing friendly pieces
                    elif end_piece[0] != self.board[row][col][0]:
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                        break
                    else: # Hit a friendly piece
                        break
        # One step S
        end_row = row + 1
        end_col = col
        if 0 <= end_row < 9 and 0 <= end_col < 9:
            end_piece = self.board[end_row][end_col]
            if end_piece == "--" or end_piece[0] != self.board[row][col][0]:
                moves.append(Move((row, col), (end_row, end_col), self.board))

    def getViceGeneralMoves(self, row, col, moves):
        """
        Vice-General moves: S, SE, SW, E, W, and one step N.
        (Logic is correct, prevents friendly fire)
        """
        directions = [(1, 0), (1, 1), (1, -1), (0, 1), (0, -1)]
        for d in directions:
            for i in range(1, 9):
                end_row = row + d[0] * i
                end_col = col + d[1] * i
                if 0 <= end_row < 9 and 0 <= end_col < 9:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    elif end_piece[0] != self.board[row][col][0]:
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                        break
                    else: # Hit a friendly piece
                        break
        # One step N
        end_row = row - 1
        end_col = col
        if 0 <= end_row < 9 and 0 <= end_col < 9:
            end_piece = self.board[end_row][end_col]
            if end_piece == "--" or end_piece[0] != self.board[row][col][0]:
                moves.append(Move((row, col), (end_row, end_col), self.board))

    def getAirMarshalMoves(self, row, col, moves):
        """
        Air Marshal moves: NE, NW, SE, SW, and N.
        (Logic is correct, prevents friendly fire)
        """
        directions = [(-1, 1), (1, 1), (-1, 0), (-1, -1), (1, -1)]
        for d in directions:
            for i in range(1, 9):
                end_row = row + d[0] * i
                end_col = col + d[1] * i
                if 0 <= end_row < 9 and 0 <= end_col < 9:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    elif end_piece[0] != self.board[row][col][0]:
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                        break
                    else: # Hit a friendly piece
                        break

    def getNavySealMoves(self, row, col, moves):
        """
        Navy Seal moves: 2 steps diagonally (NE, NW, SE, SW).
        (Logic is correct, prevents friendly fire)
        """
        directions = [(-2, 2), (2, 2), (2, -2), (-2, -2)]
        for d in directions:
            end_row = row + d[0]
            end_col = col + d[1]
            if 0 <= end_row < 9 and 0 <= end_col < 9:
                end_piece = self.board[end_row][end_col]
                if end_piece == "--" or end_piece[0] != self.board[row][col][0]:
                    moves.append(Move((row, col), (end_row, end_col), self.board))

    def getArmyBattalionMoves(self, row, col, moves):
        """
        Army Battalion moves: N, S, E, W.
        (Logic is correct, prevents friendly fire)
        """
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        for d in directions:
            for i in range(1, 9):
                end_row = row + d[0] * i
                end_col = col + d[1] * i
                if 0 <= end_row < 9 and 0 <= end_col < 9:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    elif end_piece[0] != self.board[row][col][0]:
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                        break
                    else: # Hit a friendly piece
                        break

    def getSoldierMoves(self, row, col, moves):
        """
        Soldier (Pawn) moves.
        (This logic is correct for both white and black and prevents friendly fire)
        """
        if self.white_to_move: # White moves UP (row index decreases)
            if row - 1 >= 0 and self.board[row - 1][col] == "--":
                moves.append(Move((row, col), (row - 1, col), self.board))
                if row == 7 and self.board[row - 2][col] == "--": # 2-step from row 7
                    moves.append(Move((row, col), (row - 2, col), self.board))
            if row - 1 >= 0 and col - 1 >= 0:
                if self.board[row - 1][col - 1][0] == 'b': # Correctly checks for 'b'
                    moves.append(Move((row, col), (row - 1, col - 1), self.board))
            if row - 1 >= 0 and col + 1 < 9:
                if self.board[row - 1][col + 1][0] == 'b': # Correctly checks for 'b'
                    moves.append(Move((row, col), (row - 1, col + 1), self.board))
        else: # Black moves DOWN (row index increases)
            if row + 1 < 9 and self.board[row + 1][col] == "--":
                moves.append(Move((row, col), (row + 1, col), self.board))
                if row == 1 and self.board[row + 2][col] == "--": # 2-step from row 1
                    moves.append(Move((row, col), (row + 2, col), self.board))
            if row + 1 < 9 and col - 1 >= 0:
                if self.board[row + 1][col - 1][0] == 'w': # Correctly checks for 'w'
                    moves.append(Move((row, col), (row + 1, col - 1), self.board))
            if row + 1 < 9 and col + 1 < 9:
                if self.board[row + 1][col + 1][0] == 'w': # Correctly checks for 'w'
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))


class Move:
    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False



