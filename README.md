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
