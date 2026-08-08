"""
core/player_type.py

Defines the type of player.
"""

from enum import Enum


class PlayerType(str, Enum):
    """
    Player categories.
    """

    HUMAN = "HUMAN"

    AI = "AI"

    RANDOM = "RANDOM"

    BASELINE = "BASELINE"