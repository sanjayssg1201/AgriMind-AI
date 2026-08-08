"""
brain/opponent_model.py

Opponent modelling for AgriMind AI.
"""

from brain.memory import BrainMemory
from models.game_state import GameState


class OpponentModel:
    """
    Estimates the opponent's strategy and predicts
    future behaviour.
    """

    def __init__(self, memory: BrainMemory):

        self.memory = memory

    # =====================================================
    # Economy
    # =====================================================

    def money_growth(self) -> float:

        history = self.memory.opponent_money_history

        if len(history) < 2:
            return 0

        return history[-1] - history[-2]

    def economy_strength(
        self,
        state: GameState,
    ) -> float:

        score = 0.0

        score += state.opponent.money / 100

        score += state.opponent.crops * 5

        score += state.opponent.animals * 8

        score += state.opponent.farmhands * 12

        return score

    # =====================================================
    # Expansion
    # =====================================================

    def expansion_probability(
        self,
        state: GameState,
    ) -> float:

        if not state.opponent.can_expand:
            return 0

        score = 0.0

        if state.opponent.money > 2000:
            score += 50

        score += self.money_growth() / 20

        return min(score, 100)

    # =====================================================
    # Hiring
    # =====================================================

    def hire_probability(
        self,
        state: GameState,
    ) -> float:

        if state.opponent.money < 500:
            return 0

        score = state.opponent.money / 100

        score -= state.opponent.farmhands * 8

        return max(score, 0)

    # =====================================================
    # Market
    # =====================================================

    def likely_to_sell(self) -> bool:

        return self.money_growth() <= 0

    # =====================================================
    # Strategy Detection
    # =====================================================

    def strategy(
        self,
        state: GameState,
    ) -> str:

        if state.opponent.animals > state.opponent.crops:
            return "LIVESTOCK"

        if state.opponent.crops > state.opponent.animals:
            return "CROPS"

        if state.opponent.farmhands >= 3:
            return "AUTOMATION"

        if state.opponent.money > 4000:
            return "ECONOMY"

        return "BALANCED"

    # =====================================================
    # Threat
    # =====================================================

    def threat_level(
        self,
        state: GameState,
    ) -> float:

        score = 0.0

        if state.opponent_money > state.money:
            score += 25

        score += self.economy_strength(state)

        score += self.expansion_probability(state)

        return score

    # =====================================================
    # Prediction
    # =====================================================

    def predict_next_action(
        self,
        state: GameState,
    ) -> str:

        if self.expansion_probability(state) > 70:
            return "EXPAND"

        if self.hire_probability(state) > 60:
            return "HIRE"

        if self.likely_to_sell():
            return "SELL"

        return self.strategy(state)