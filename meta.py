import math


class GameMeta:
    """
    Contains meta information and constants for the game configuration.
    """
    # Player identifiers
    PLAYERS = {
        'none': 0,
        'one': 1,
        'two': 2
    }

    # Game outcomes
    OUTCOMES = {
        'none': 0,
        'one': 1,
        'two': 2,
        'draw': 3
    }

    # Infinity value for search algorithms
    INF = float('inf')

    # Board dimensions
    ROWS = 6
    COLS = 7


class MCTSMeta:
    """
    Contains meta information for the Monte Carlo Tree Search configuration.
    """
    # Exploration constant for the UCT formula
    EXPLORATION = math.sqrt(2)
