"""
core/game_mode.py

Supported game modes.
"""

from enum import Enum


class GameMode(str, Enum):
    """
    Supported gameplay modes.
    """

    HUMAN_VS_HUMAN = "HUMAN_VS_HUMAN"

    HUMAN_VS_AI = "HUMAN_VS_AI"

    AI_VS_AI = "AI_VS_AI"

    TOURNAMENT = "TOURNAMENT"

    TRAINING = "TRAINING"

    DEBUG = "DEBUG"

    EVALUATION = "EVALUATION"