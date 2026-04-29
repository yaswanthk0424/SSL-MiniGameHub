
<h1 align="center">Mini Game Hub </h1>




# MiniGameHub — Usage Guide

## Setup and Launch
1. Download the project `.tgz` file.
2. Extract it using:
```bash
   tar -xvzf submission.tgz
```
3. Open a terminal and navigate to the extracted folder:
```bash
   cd submission/hub
```
4. Run the application:
```bash
   bash main.sh
```

---

## Login / Registration
- On launching the application, you will be prompted to either **register** or **log in**.
- Two players are required to enter their **usernames and passwords**.

**Notes:**
- If a username already exists, you will be asked to enter a different one.
- If passwords do not match during registration, you will be prompted to re-enter them.

---

## Game Selection
- After successful login, a **game menu interface** will be displayed.
- Select the game you want to play using the GUI.

---

## Gameplay
- The selected game will open in a **Pygame window**.
- Follow the **on-screen instructions** to play.

---

## After Gameplay
- Once the game ends, you will be returned to the **main menu**.
- You can:
  - Play another game
  - Exit the application


# Preliminary plan

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

