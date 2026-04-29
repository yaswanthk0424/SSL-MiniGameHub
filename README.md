<<<<<<< Updated upstream
<h1 align="center">Mini Game Hub </h1>

## Project Idea

This project implements a secure, multi-user **Mini Game Hub** using **Bash** for authentication and **Python (Pygame)** for gameplay.
Two authenticated users can select and play board games through a graphical interface, with results recorded and shown through a leaderboard system.

---
## Proposed Features

* Secure user authentication using SHA-256 hashing
* Multiple board games:

  * Tic-Tac-Toe (10×10, 5-in-a-row)
  * Othello (Reversi)
  * Connect Four
*  Graphical interface using Pygame (no terminal gameplay)
* Multiple Game Themes
* Leaderboard highlighting player's current position and sorted according to a specified metric.
* Leaderboard is shown after every game and can also be viewed through options. 
* Data visualization using Matplotlib (charts and graphs)


---

## System Design
The project is divided into distinct components

### Workflow
 
1. main.sh -> User Authentication -> game.py -> Game Selection -> game menu -> play

2. history.csv update

3. leaderboard.sh

4. Matplotlib Visualization

5. Return to game menu 

---


## High-Level Implementation Plan

### Phase 1: Design & Setup

* Create project structure
* Implement authentication system (main.sh)
* Design base class for board games

### Phase 2: Core Game Development

* Implement Tic-Tac-Toe, Othello, and Connect Four
* Integrate NumPy for board representation
* Build Pygame GUI for gameplay

### Phase 3: Data Handling & Leaderboard

* Store results in history.csv
* Implement leaderboard.sh for statistics
* Enable sorting based on performance metrics

### Phase 4: Visualization

* Generate charts using Matplotlib
* Improve UI and user experience

---
=======
# SSL-MiniGameHub
>>>>>>> Stashed changes
