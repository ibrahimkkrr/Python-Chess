# ♟️ Python MVC Chess Engine

A fully functional, object-oriented Chess Engine built from scratch using Python and Pygame. 

This project was refactored from a procedural "scuffed" codebase into a strict **Model-View-Controller (MVC)** architecture. It features full legal move validation, advanced rules (Castling, Pawn Promotion), and a custom Minimax AI opponent.

---

## 🏗️ System Architecture

The codebase adheres strictly to the MVC design pattern, utilizing a central Controller to mediate between the Pygame UI (View) and the pure-Python chess logic (Model).

```mermaid
classDiagram
    class ChessGameController {
        +ChessEngine engine
        +ChessView view
        +ControllerState state
        +handle_events()
        +update()
    }

    class ChessEngine {
        +Board board
        +make_move()
        +get_ai_move()
    }

    class ChessView {
        +Dictionary images
        +ViewState state
        +render(engine)
    }

    ChessGameController --> ChessEngine : Modifies Data
    ChessGameController --> ChessView : Triggers Render
    ChessView ..> ChessEngine : Reads Data (Read-Only)

## 📐 Detailed Class Blueprint

For a complete deep-dive into the design patterns used, expand the complete system diagram below.

<details>
<summary><b>🔍 Click to expand the Full System Blueprint (All Classes & Relations)</b></summary>


classDiagram
    %% ==========================================
    %% 0. THE APPLICATION ROOT
    %% ==========================================
    class ChessApp {
        +Surface screen
        +Int square_size
        +Boolean running
        +ChessEngine engine
        +ChessView view
        +ChessGameController active_controller
        +change_controller(new_controller)
        +run()
    }

    ChessApp *-- ChessGameController : manages
    ChessApp *-- ChessEngine : initializes
    ChessApp *-- ChessView : initializes

    %% ==========================================
    %% 1. THE CONTROLLER (Input Management)
    %% ==========================================
    class ChessGameController {
        +ChessEngine engine
        +ChessView view
        +ControllerState state
        +handle_events(events, square_size)
        +update(dt)
        +render(screen, square_size)
        +change_state(new_state)
    }

    class ControllerState {
        <<Abstract>>
        +handle_mouse_click(controller, x, y)*
        +update(controller, dt)*
    }

    class ControllerMainMenuState
    class ControllerPlayingState
    class ControllerGameOverState
    class ControllerPauseState
    class ControllerPromotingState

    ChessGameController o-- ControllerState : Current State
    ControllerState <|-- ControllerMainMenuState
    ControllerState <|-- ControllerPlayingState
    ControllerState <|-- ControllerGameOverState
    ControllerState <|-- ControllerPauseState
    ControllerState <|-- ControllerPromotingState

    %% ==========================================
    %% 2. THE VIEW (Rendering & UI)
    %% ==========================================
    class ChessView {
        +Dictionary images
        +Dictionary sounds
        +ViewState state
        +render(screen, square_size, engine, legal_moves)
        +play_sound(key)
        +change_state(new_state)
    }

    class ViewState {
        <<Abstract>>
        +render(screen, square_size, engine, view, legal_moves)*
    }

    class ViewMainMenuState
    class ViewPlayingState
    class ViewGameOverState
    class ViewPauseState
    class ViewPromotingState

    ChessView o-- ViewState : Current State
    ViewState <|-- ViewMainMenuState
    ViewState <|-- ViewPlayingState
    ViewState <|-- ViewGameOverState
    ViewState <|-- ViewPauseState
    ViewState <|-- ViewPromotingState

    %% ==========================================
    %% 3. THE MODEL (Engine & Board)
    %% ==========================================
    class ChessEngine {
        +Board board
        +String turn
        +Boolean is_game_over
        +make_move(start, target)
        +get_valid_moves(row, col)
        +get_ai_move()
        +evaluate_board()
        +is_king_in_check()
    }

    class Board {
        -List matrix
        +get_piece(row, col)
        +move_piece(start_row, start_col, end_row, end_col)
        +is_on_board(row, col)
        -_create_empty_matrix()
    }

    class PieceFactory {
        <<Static>>
        +create_piece(symbol)$ Piece
    }

    ChessGameController --> ChessEngine : Updates logic
    ChessGameController --> ChessView : Triggers render
    ChessView ..> ChessEngine : Reads state (Read-Only)

    ChessEngine *-- Board : Owns
    Board ..> PieceFactory : Uses to build board

    %% ==========================================
    %% 4. THE PIECES (Strategy Pattern)
    %% ==========================================
    class Piece {
        <<Abstract>>
        +String color
        +String name
        +Boolean has_moved
        +get_raw_moves(row, col, board)*
    }

    class Queen {
        -Rook rook
        -Bishop bishop
        +get_raw_moves()
    }
    class King {
        +get_castle_moves()
        +get_raw_moves()
    }
    class Pawn {
        +get_raw_moves()
    }
    class Rook
    class Bishop
    class Knight

    Board o-- Piece : Contains
    PieceFactory ..> Piece : Instantiates

    Piece <|-- Queen
    Piece <|-- King
    Piece <|-- Pawn
    Piece <|-- Rook
    Piece <|-- Bishop
    Piece <|-- Knight

    Queen *-- Rook : Composes
    Queen *-- Bishop : Composes
