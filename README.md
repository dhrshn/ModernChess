# ClassicWarfareChess


# 9x9 Chess Game

![Game Screenshot](https://i.imgur.com/xyz1234.png)  
*(Replace with an actual screenshot if you have one.)*

## Description
This is a **9x9 Chess Game** with custom pieces, unique movement rules, and special abilities. Players can enjoy a strategic and engaging chess variant with features like turn-based play, move highlighting, undo/redo functionality, and a timer. Built using Python and Tkinter for the GUI.

## Features
- **Custom 9x9 Board**: A larger board for more complex gameplay.
- **Unique Piece Movements**: Each piece has its own movement mechanics.
- **Special Abilities**: Unique abilities for each piece, such as reviving soldiers, air strikes, and stealth.
- **Turn-Based Play**: Players take turns, and the game enforces strict turn order.
- **Move Highlighting**: Valid moves for the selected piece are highlighted.
- **Undo/Redo Functionality**: Players can undo or redo their moves.
- **Timer**: Each player has a timer to track their remaining time.
- **GUI**: Clean and intuitive interface built using Tkinter.




## Key Features

### Expanded 9x9 Board
- A larger grid with additional rows and columns for deeper strategic gameplay.

### Unique Piece Movements
Each piece has distinct movement patterns:

- **President** – Moves one step in any direction.
- **General** – Moves across the board in **N, NE, NW, E**, and takes one step **S**.
- **Vice-General** – Moves across the board in **S, SE, SW, E, W**, and takes one step **N**.
- **Air Marshal** – Moves in **NE-W, SE-W, and N** directions.
- **Navy Seal** – Moves in a unique **two-step pattern with directional turns**.
- **Army Battalion** – Moves in straight lines across **N, S, E, W**.
- **Soldier** – Moves like a traditional chess **pawn**.

### Special Abilities
- **President's Call to Arms** – Revive a captured Soldier.
- **General’s Rally** – Grant a free move to an adjacent piece.
- **Vice-General’s Fortify** – Create a defensive position.
- **Air Marshal’s Air Strike** – Eliminate an enemy piece within a 3-square radius.
- **Navy Seal’s Stealth** – Become invisible for one turn.

### Gameplay Mechanics
- **Turn-Based Play** – Players take turns, following a strict turn order.
- **Move Highlighting** – Displays valid moves when a piece is selected.
- **Undo/Redo Functionality** – Allows players to revert or reapply moves.
- **Timer** – Each player has a countdown timer to manage their turns.
- **Graphical User Interface (GUI)** – Built with **Tkinter** for an intuitive experience.

---

## Technologies Used
- **Python** – Core language for game logic.
- **Tkinter** – GUI framework for smooth user interaction.
- **PIL (Pillow)** – Handles loading and resizing of piece images.

---

## How to Play

1. **Select a Piece** – Click on a piece to highlight its valid moves.
2. **Make a Move** – Click on a highlighted square to move the piece.
3. **Use Special Abilities** – Select a piece with an ability and follow on-screen prompts.
4. **Undo/Redo** – Use the "Undo" and "Redo" buttons to adjust moves.
5. **Manage Time** – Keep track of the timer to avoid running out of time.

---

## Project Structure
- **`chessengine.py`** – Contains the core game logic, including piece movements and special abilities.
- **`chessui.py`** – Handles the graphical interface using Tkinter.
- **`images/`** – Directory containing piece images.
- **`README.md`** – Documentation for the project.

---

## Contributing
We welcome contributions! To contribute:
1. **Fork** the repository.
2. **Create a new branch** for your feature or bug fix.
3. **Commit** your changes.
4. **Submit a pull request** for review.

---

## License
This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

## Acknowledgments
- Inspired by traditional chess and modern strategy games.
- Developed using **Python and Tkinter**.










 
