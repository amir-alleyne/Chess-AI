# Chess AI Simulation

## Overview
The **Chess AI Simulation** is a Minichess-based artificial intelligence system that utilizes game trees and different player strategies to simulate and improve chess gameplay. The project consists of multiple AI-controlled players, each employing different approaches such as random move selection, greedy decision-making, and reinforcement learning.

## Features
- **Game Tree Construction:** Generates and utilizes game trees to analyze and simulate gameplay.
- **AI Players:**
  - **RandomTreePlayer:** Selects moves randomly based on a game tree.
  - **GreedyTreePlayer:** Selects moves with the highest probability of winning.
  - **ExploringPlayer:** A reinforcement learning-based player that balances exploration and exploitation.
- **Simulation & Learning:** Implements a learning algorithm that improves decision-making over time.
- **Minichess Support:** Operates on a smaller chess board, making it suitable for efficient AI learning and experimentation.
- **Statistics & Analysis:** Tracks game results and allows visualization of player performance.


## AI Strategies
### 1. **RandomTreePlayer**
- Loads a game tree from past game data.
- Moves are chosen randomly within the tree.
- If the tree doesn’t contain the opponent’s move, a move is picked randomly.

### 2. **GreedyTreePlayer**
- Constructs a complete game tree up to depth `d`.
- Selects the move with the highest probability of winning.
- Balances offense and defense based on win probabilities.

### 3. **ExploringPlayer (Reinforcement Learning)**
- Plays games while balancing exploration (trying new moves) and exploitation (choosing the best-known move).
- Updates the game tree after each game.
- Exploration probability decreases over time to favor better moves.
