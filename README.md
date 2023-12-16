# Flappy Bird Game in Python

## Overview
This repository contains the source code for a simple Flappy Bird game implemented in Python using the Pygame library. The game includes features such as sound effects, music, score tracking, high score recording, and a restart counter.

## Features

### 1. Game Mechanics
- **Flappy Bird Movement:** The player controls a bird that can jump by pressing the spacebar, navigating through pipes.
- **Collision Detection:** The game checks for collisions with pipes and the ground to determine when the game should end.

### 2. Sound and Music
- **Sound Effects:** Various sound effects are implemented, including flapping wings, collision sounds, and point scoring sounds.
- **Background Music:** The game features background music that plays throughout the gameplay.

### 3. Score Tracking
- **Score Counter:** The game keeps track of the player's score, incrementing it each time the bird successfully passes through a pair of pipes.
- **High Score Counter:** The high score is recorded and updated if the player achieves a new high score.

### 4. Restart Counter
- **Restart Counter:** A counter keeps track of how many times the game has been restarted, providing insights into the player's persistence.

## Getting Started

### Prerequisites
- Python 3.x
- Pygame library (`pip install pygame`)

### Running the Game
1. Clone the repository: `git clone https://github.com/your-username/flappy-bird-python.git`
2. Navigate to the project directory: `cd flappy-bird-python`
3. Run the game: `python flappy_bird.py`

## Code Structure
- `flappy_bird.py`: Main game script containing the game loop and logic.
- `sprites/`: Directory containing sprite images for the bird, pipes, and background.
- `sounds/`: Directory containing sound files for the game.

## Acknowledgments
- Inspired by the original Flappy Bird game created by Dong Nguyen.
- Pygame library for simplifying game development in Python.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Author
[Your Name]

Feel free to contribute to the project or use the code as a base for your own projects. If you encounter any issues or have suggestions, please open an issue. Enjoy playing Flappy Bird!
