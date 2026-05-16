# 🏗 Software Architecture & Design Patterns

## 1. MVC (Model-View-Controller) Architectural Pattern
To solve the "God Class" problem identified in Phase 0 (where the engine handled logic, rendering, and inputs simultaneously), the codebase was refactored into a strict MVC structure:
* **Model (`src/engine/`):** Contains pure Python chess logic (`board.py`, `pieces.py`). It has absolutely no knowledge of Pygame or the screen.
* **View (`src/view/`):** Handles all Pygame rendering, drawing sprites, and displaying menus.
* **Controller (`src/controller/`):** Listens for mouse clicks and keyboard events, routing them to the appropriate state.

## 2. State Pattern
To eliminate complex, nested `if/elif` blocks for menu navigation, the State Pattern was implemented. 
* The game relies on State Managers (`manager.py`) to transition seamlessly between `state_main_menu`, `state_playing`, `state_pause`, and `state_game_over`. 
* Each state implements its own specific rules for what inputs to listen to and what graphics to draw, making adding new menus completely modular.

## 3. Simple Factory Pattern (`PieceFactory`)
* **The Problem:** When initializing the board from a text grid (like `'r', 'n', 'b'`), the `Board` class would need a massive, repetitive `if/else` block to figure out which piece object to instantiate and what color it should be.
* **The Solution:** Implemented the **Factory Pattern** via the `PieceFactory` class. The board simply passes a string character to `PieceFactory.create_piece(symbol)`, and the factory abstracts away the complex instantiation logic, returning a fully formed `Piece` object.
* **Result:** The `Board` class is decoupled from the specific Piece classes. Adding a new piece type only requires one new line in the Factory, adhering to the Open/Closed Principle.

## 4. Strategy Pattern & Polymorphism (`Piece` Hierarchy)
* **The Problem:** In Phase 0, all piece movement logic was crammed into a single bloated class, violating the Single Responsibility Principle.
* **The Solution:** Implemented the **Strategy Pattern** using an Abstract Base Class (`Piece`). Each specific piece (`Knight`, `Rook`, `Pawn`, etc.) is a subclass that implements its own version of the `@abstractmethod def get_raw_moves()`. 
* **Result:** When the Engine needs to know where a piece can move, it simply calls `piece.get_raw_moves()`. It doesn't need to know *what* the piece is; it trusts the piece to calculate its own geometric strategy.

## 5. Composition Over Inheritance (The `Queen` Class)
* **The Problem:** A Queen moves like both a Rook and a Bishop. Copying and pasting the movement loops from the `Rook` and `Bishop` classes into the `Queen` class would violate the DRY (Don't Repeat Yourself) principle.
* **The Solution:** Used **Object Composition**. Inside the `Queen`'s `__init__`, it instantiates its own internal private `Rook` and `Bishop` objects. When asked for its moves, the Queen simply delegates the math to those two objects and adds their lists together.

* ## 6. Encapsulation & Data Abstraction (`Board` Class)
* **The Problem:** In Phase 0, the internal 2D array of the board was exposed. The game Engine was directly manipulating `board.matrix[row][col]`, which led to scattered logic, potential crashes, and a "helpless" board that couldn't validate its own state.
* **The Solution:** Implemented strict **Encapsulation**. The 2D array (`self.matrix`) is now treated as private. The Engine is forced to interact with the board exclusively through controlled API methods like `get_piece()` and `move_piece()`.
* **Result:** The Board is now responsible for its own complex internal state changes. For example, when castling, the Engine simply tells the Board to move the King by two squares. The `move_piece()` method automatically detects this and secretly teleports the corresponding Rook, entirely abstracting that complex operation away from the main Engine loop.

## 7. Mediator Pattern (`ChessEngine`)
* **The Problem:** If Pieces, the Board, and the Game State all communicate directly with each other, it creates a tightly coupled "spaghetti" system. For example, a Piece shouldn't be responsible for knowing if its move puts its own King in check.
* **The Solution:** The `ChessEngine` acts as the **Mediator**. The UI/Controller only talks to the Engine. The Engine coordinates the `Board`, queries the `Piece` objects for their raw geometry, and determines the rules of chess (turns, checkmate, castling). 
* **Result:** Total decoupling. The components are isolated and only interact through the central Engine hub.

## 8. Prototype Pattern / State Cloning (Move Validation & AI)
* **The Problem:** To know if a move is legal, the game needs to know if that move will result in the King being in check *in the future*. 
* **The Solution:** Used the **Prototype Pattern** concept via Python's `copy.deepcopy()`. Instead of temporarily moving pieces on the live board (which is highly prone to bugs and crashing), the Engine creates a "ghost" clone of the board, plays the move in an alternate universe, and evaluates the danger.
* **Result:** Safe, bug-free move validation and AI look-ahead simulation without ever corrupting the real game state.

## 9. Minimax Algorithm (The AI Engine)
* **The Problem:** The game needed a single-player mode, requiring an AI that doesn't just make random moves, but actively tries to win.
* **The Solution:** Implemented a lightweight version of the **Minimax Algorithm** in `get_ai_move()`. The AI simulates its own possible moves, then simulates the human's best possible counter-attacks, and mathematically scores the board using piece values (King=900, Queen=90) to find the path of least damage.
* **Result:** A functioning, competitive AI that actively defends its pieces and threatens the player.

## 10. State Pattern (UI & Render Management)
* **The Problem:** In Phase 0, handling different screens (Main Menu, Playing, Pause, Game Over) required massive, deeply nested `if/elif` blocks inside the main render loop. Adding a new screen meant risking breaking the entire game loop.
* **The Solution:** Implemented the **State Pattern**. The `ChessView` class acts as the Context. It holds a `self.state` object (like `ViewMainMenuState` or `ViewPlayingState`). When `ChessView.render()` is called, it blindly delegates the rendering to its current state object.
* **Result:** Zero `if` statements in the render loop. To add a new screen (like a "Settings" menu), we just create a new State class without ever touching the core `ChessView` code.

## 11. Flyweight Pattern / Resource Manager (Asset Loading)
* **The Problem:** Loading `.png` images and `.mp3` sounds from the hard drive is incredibly slow. If the game loaded the image of a Pawn every single time it drew a Pawn on the screen (60 frames per second), the game's memory would bloat and crash.
* **The Solution:** Implemented a Resource Manager acting as a **Flyweight**. The `load_images()` and `__init__` functions load all `.png` and `.mp3` files from the disk exactly *once* at startup and store them in memory dictionaries (`self.images` and `self.sounds`).
* **Result:** When the engine draws 16 Pawns, it is just passing 16 lightweight references to the exact same image in memory, resulting in buttery-smooth 60 FPS rendering.

## 12. State Pattern (Input & Event Handling)
* **The Problem:** Processing mouse clicks and keyboard presses is entirely different depending on the current screen. Clicking the center of the screen in the Main Menu should trigger a "Play" button, but doing the exact same click during gameplay should select a chess piece. Handling this in a single loop would require massive, nested `if current_screen == "playing":` blocks.
* **The Solution:** Implemented the **State Pattern** for the Controller. The `ChessGameController` intercepts raw Pygame events (`MOUSEBUTTONDOWN`, `KEYDOWN`) and blindly delegates them to its current `self.state` object.
* **Result:** Total separation of input logic. The Main Menu state only listens for button clicks, while the Playing state calculates grid coordinates to select pieces.

## 13. MVC Orchestration (The Controller)
* **The Problem:** If the UI directly modified the chess board, and the board directly triggered UI sounds, the codebase would become permanently tangled.
* **The Solution:** The `ChessGameController` acts as the definitive bridge. It holds a reference to both the `engine` (Model) and the `view` (View). When the user clicks, the Controller's state tells the Engine to update the logic, and then the Controller immediately tells the View to render the new reality.
* **Result:** The Engine and the View never talk to each other directly, ensuring strict separation of concerns.

