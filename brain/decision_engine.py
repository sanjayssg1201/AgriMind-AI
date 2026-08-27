"""
brain/decision_engine.py

Master decision engine for AgriMind AI.

Combines:
- task generation
- worker scheduling
- action evaluation
- economy intelligence
- risk analysis
- opponent modelling
- strategic planning
- future planning
- memory
"""

from typing import Any

from brain.memory import BrainMemory
from brain.task_generator import TaskGenerator
from brain.scheduler import Scheduler
from brain.evaluator import Evaluator
from brain.economy import EconomyManager
from brain.risk_analyzer import RiskAnalyzer
from brain.opponent_model import OpponentModel
from brain.strategy_intelligence import StrategyIntelligence
from brain.strategic_planner import StrategicPlanner
from brain.future_planner import FuturePlanner
from brain.action_candidate import ActionCandidate

from models.game_state import GameState


class DecisionEngine:
    """
    Main AI controller.

    Converts a GameState into the highest-scoring
    ActionCandidate.
    """

    def __init__(self):

        # -------------------------------------------------
        # Core memory
        # -------------------------------------------------

        self.memory = BrainMemory()

        # -------------------------------------------------
        # Decision pipeline
        # -------------------------------------------------

        self.task_generator = TaskGenerator()

        self.scheduler = Scheduler()

        self.evaluator = Evaluator(
            self.memory
        )

        # -------------------------------------------------
        # Intelligence layers
        # -------------------------------------------------

        self.economy = EconomyManager(
            self.memory
        )

        self.risk = RiskAnalyzer(
            self.memory
        )

        self.opponent = OpponentModel(
            self.memory
        )

        self.strategy = StrategyIntelligence(
            self.economy
        )

        self.strategic_planner = StrategicPlanner(
            self.strategy
        )

        self.future_planner = FuturePlanner()

    # =====================================================
    # Public API
    # =====================================================

    def decide(
        self,
        state: GameState,
    ) -> ActionCandidate | None:
        """
        Return the best action for the current turn.
        """

        # -------------------------------------------------
        # Update memory
        # -------------------------------------------------

        self.memory.update(
            state
        )

        # -------------------------------------------------
        # Generate tasks
        # -------------------------------------------------

        tasks = self.task_generator.generate(
            state
        )

        if not tasks:
            return None

        # -------------------------------------------------
        # Assign workers
        # -------------------------------------------------

        candidates = self.scheduler.assign(
            state,
            tasks,
        )

        if not candidates:
            return None

        # -------------------------------------------------
        # Evaluate candidates
        # -------------------------------------------------

        evaluated = []

        for candidate in candidates:

            evaluated.append(
                self.evaluator.evaluate(
                    state,
                    candidate,
                )
            )

        if not evaluated:
            return None

        # -------------------------------------------------
        # Select best candidate
        # -------------------------------------------------

        best = self._select_best(
            state,
            evaluated,
        )

        # -------------------------------------------------
        # Remember selected action
        # -------------------------------------------------

        if best is not None:

            self.memory.remember_action(
                best.action,
                best.score,
            )

        return best

    # =====================================================
    # Selection
    # =====================================================

    def _select_best(
        self,
        state: GameState,
        candidates: list[ActionCandidate],
    ) -> ActionCandidate | None:
        """
        Apply global intelligence adjustments and return
        the highest final-scoring candidate.
        """

        if not candidates:
            return None

        for candidate in candidates:

            self._apply_global_adjustments(
                state,
                candidate,
            )

        candidates.sort(
            key=lambda candidate: candidate.final_score,
            reverse=True,
        )

        return candidates[0]

    # =====================================================
    # Global Score Adjustment
    # =====================================================

    def _apply_global_adjustments(
        self,
        state: GameState,
        candidate: ActionCandidate,
    ) -> None:
        """
        Apply all high-level intelligence layers.
        """

        score = candidate.score

        # -------------------------------------------------
        # Economy
        # -------------------------------------------------

        score += self._economy_bonus(
            state,
            candidate,
        )

        # -------------------------------------------------
        # Risk
        # -------------------------------------------------

        score -= self._risk_penalty(
            state,
            candidate,
        )

        # -------------------------------------------------
        # Opponent
        # -------------------------------------------------

        score += self._opponent_bonus(
            state,
            candidate,
        )

        # -------------------------------------------------
        # Strategic Planning
        # -------------------------------------------------

        score += self._strategic_bonus(
            state,
            candidate,
        )

        # -------------------------------------------------
        # Future Planning
        # -------------------------------------------------

        score += self._future_bonus(
            state,
            candidate,
        )

        candidate.score = score

    # =====================================================
    # Economy Bonus
    # =====================================================

    def _economy_bonus(
        self,
        state: GameState,
        candidate: ActionCandidate,
    ) -> float:
        """
        Adjust candidate score using market/economic
        intelligence.
        """

        task = candidate.task

        # -------------------------------------------------
        # SELL
        # -------------------------------------------------

        if task == "SELL":

            product = candidate.target

            if not product:
                return 0.0

            price = state.market.price(
                product
            )

            if self.economy.should_sell(
                product,
                price,
            ):
                return 20.0

            dynamic_score = (
                self.economy.dynamic_market_score(
                    state,
                    product,
                )
            )

            if dynamic_score > 0:
                return float(
                    dynamic_score
                )

            return -15.0

        # -------------------------------------------------
        # BUY PRODUCT
        # -------------------------------------------------

        if task == "BUY_PRODUCT":

            product = candidate.target

            if not product:
                return 0.0

            dynamic_score = (
                self.economy.dynamic_market_score(
                    state,
                    product,
                )
            )

            return float(
                dynamic_score
            )

        # -------------------------------------------------
        # BUY SEED
        # -------------------------------------------------

        if task == "BUY_SEED":

            return 5.0

        # -------------------------------------------------
        # BUY ANIMAL
        # -------------------------------------------------

        if task == "BUY_ANIMAL":

            return 5.0

        return 0.0

    # =====================================================
    # Risk Penalty
    # =====================================================

    def _risk_penalty(
        self,
        state: GameState,
        candidate: ActionCandidate,
    ) -> float:
        """
        Apply risk-based penalties.

        RiskAnalyzer implementations may expose different
        helper methods, so this layer remains defensive.
        """

        task = candidate.task

        # -------------------------------------------------
        # Try task-specific risk score
        # -------------------------------------------------

        try:

            if hasattr(
                self.risk,
                "risk_score",
            ):

                risk_score = self.risk.risk_score(
                    state,
                    candidate,
                )

                if risk_score is not None:
                    return max(
                        0.0,
                        float(risk_score),
                    )

        except (
            AttributeError,
            TypeError,
            ValueError,
        ):
            pass

        # -------------------------------------------------
        # Market concentration risk
        # -------------------------------------------------

        if task == "BUY_PRODUCT":

            product = candidate.target

            if product:

                try:

                    risk_score = (
                        self.economy.market_risk_score(
                            state,
                            product,
                        )
                    )

                    return max(
                        0.0,
                        float(risk_score) * 0.25,
                    )

                except (
                    AttributeError,
                    TypeError,
                    ValueError,
                ):
                    pass

        return 0.0

    # =====================================================
    # Opponent Bonus
    # =====================================================

    def _opponent_bonus(
        self,
        state: GameState,
        candidate: ActionCandidate,
    ) -> float:
        """
        Adjust the score according to opponent behaviour.
        """

        try:

            if hasattr(
                self.opponent,
                "action_bonus",
            ):

                value = self.opponent.action_bonus(
                    state,
                    candidate,
                )

                if value is not None:
                    return float(value)

        except (
            AttributeError,
            TypeError,
            ValueError,
        ):
            pass

        try:

            if hasattr(
                self.opponent,
                "strategic_pressure",
            ):

                value = self.opponent.strategic_pressure(
                    state,
                    candidate,
                )

                if value is not None:
                    return float(value)

        except (
            AttributeError,
            TypeError,
            ValueError,
        ):
            pass

        return 0.0

    # =====================================================
    # Strategic Bonus
    # =====================================================

    def _strategic_bonus(
        self,
        state: GameState,
        candidate: ActionCandidate,
    ) -> float:
        """
        Apply strategic-planner guidance.
        """

        try:

            recommendation = (
                self.strategy.risk_adjusted_recommendation(
                    state
                )
            )

        except (
            AttributeError,
            TypeError,
            ValueError,
        ):

            return 0.0

        task = candidate.task

        # -------------------------------------------------
        # Strategic alignment
        # -------------------------------------------------

        if (
            recommendation == "GROW"
            and task in (
                "PLANT",
                "WATER",
                "FERTILIZE",
            )
        ):
            return 10.0

        if (
            recommendation == "PRODUCE"
            and task in (
                "PLANT",
                "HARVEST",
                "WATER",
            )
        ):
            return 10.0

        if (
            recommendation == "BUILD_LIVESTOCK"
            and task == "BUY_ANIMAL"
        ):
            return 15.0

        if (
            recommendation == "EXPAND"
            and task == "EXPAND"
        ):
            return 15.0

        if (
            recommendation == "OPTIMIZE_MARKET"
            and task in (
                "SELL",
                "BUY_PRODUCT",
            )
        ):
            return 10.0

        if (
            recommendation == "PRESERVE_CAPITAL"
            and task in (
                "BUY_PRODUCT",
                "BUY_ANIMAL",
                "EXPAND",
                "HIRE",
            )
        ):
            return -15.0

        return 0.0

    # =====================================================
    # Future Bonus
    # =====================================================

    def _future_bonus(
        self,
        state: GameState,
        candidate: ActionCandidate,
    ) -> float:

        future_score = self.future_planner.score(
            state,
            candidate,
        )

        if future_score <= 0:
            return 0.0

        return future_score * 0.5

    def _learning_bonus(
        self,
        candidate: ActionCandidate,
    ) -> float:
        """Adjust score using historical performance of this action type."""

        action_type = candidate.action

        success_rate = self.memory.strategy_success_rate(
            action_type
        )

        if success_rate == 0.5:
            return 0.0

        bonus = (success_rate - 0.5) * 20.0

        return max(-10.0, min(10.0, bonus))

    # =====================================================
    # Experience Learning
    # =====================================================

    def record_outcome(
        self,
        action: ActionCandidate | Any,
        reward: float,
        metadata: dict | None = None,
    ) -> None:
        """
        Record the result of a previously selected action.

        This allows BrainMemory to accumulate action/reward
        experiences for future learning.
        """

        if isinstance(
            action,
            ActionCandidate,
        ):

            action_name = action.action

            if metadata is None:
                metadata = {}

            metadata = {
                **metadata,
                "task": action.task,
                "target": action.target,
                "score": action.score,
            }

        else:

            action_name = action

        self.memory.remember_experience(
            action_name,
            reward,
            metadata,
        )

        self.memory.remember_outcome(
            {
                "action": action_name,
                "reward": float(reward),
                "metadata": metadata or {},
            }
        )

    

    # =====================================================
    # Memory Helpers
    # =====================================================

    def reset(self) -> None:
        """
        Reset the decision engine's persistent memory.
        """

        self.memory.reset()

    def action_average_reward(
        self,
        action: Any,
    ) -> float:
        """
        Return historical average reward for an action.
        """

        return self.memory.action_average_reward(
            action
        )

    def action_experience_count(
        self,
        action: Any,
    ) -> int:
        """
        Return the number of historical experiences
        for an action.
        """

        return self.memory.action_experience_count(
            action
        )

    # =====================================================
    # Debug
    # =====================================================

    def __repr__(self) -> str:

        return (
            "DecisionEngine("
            f"states={self.memory.state_count}, "
            f"actions={self.memory.action_count}, "
            f"experiences={self.memory.experience_count}"
            ")"
        )