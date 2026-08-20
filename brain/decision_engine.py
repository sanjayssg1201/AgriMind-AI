"""
brain/decision_engine.py

Master decision engine for AgriMind AI.
"""

from brain.memory import BrainMemory
from brain.task_generator import TaskGenerator
from brain.scheduler import Scheduler
from brain.evaluator import Evaluator
from brain.economy import EconomyManager
from brain.risk_analyzer import RiskAnalyzer
from brain.opponent_model import OpponentModel
from brain.strategy_intelligence import StrategyIntelligence
from brain.action_candidate import ActionCandidate

from models.game_state import GameState


class DecisionEngine:
    """
    Main AI controller.

    Responsible for converting a GameState into the
    highest-scoring ActionCandidate.
    """

    def __init__(self):

        self.memory = BrainMemory()

        self.task_generator = TaskGenerator()

        self.scheduler = Scheduler()

        self.evaluator = Evaluator(
            self.memory
        )

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

    # =====================================================
    # Public API
    # =====================================================

    def decide(
        self,
        state: GameState,
    ) -> ActionCandidate | None:
        """
        Returns the best action for this turn.
        """

        # --------------------------------------------
        # Update memory
        # --------------------------------------------

        self.memory.update(state)

        # --------------------------------------------
        # Generate tasks
        # --------------------------------------------

        tasks = self.task_generator.generate(
            state
        )

        if not tasks:

            return None

        # --------------------------------------------
        # Assign workers
        # --------------------------------------------

        candidates = self.scheduler.assign(
            state,
            tasks,
        )

        if not candidates:

            return None

        # --------------------------------------------
        # Evaluate candidates
        # --------------------------------------------

        evaluated = []

        for candidate in candidates:

            evaluated.append(

                self.evaluator.evaluate(
                    state,
                    candidate,
                )

            )
        

        # --------------------------------------------
        # Select best candidate
        # --------------------------------------------

        best = self._select_best(
            state,
            evaluated,
        )

        if best:

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

        raise NotImplementedError
    # =====================================================
    # Selection
    # =====================================================

    def _select_best(
        self,
        state: GameState,
        candidates: list[ActionCandidate],
    ) -> ActionCandidate | None:

        if not candidates:
            return None

        for candidate in candidates:

            self._apply_global_adjustments(
                state,
                candidate,
            )

        candidates.sort(
            key=lambda c: c.final_score,
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

        score = candidate.score

        # --------------------------------------------
        # Economy
        # --------------------------------------------

        score += self._economy_bonus(
            state,
            candidate,
        )

        # --------------------------------------------
        # Risk
        # --------------------------------------------

        score -= self._risk_penalty(
            state,
            candidate,
        )

        # --------------------------------------------
        # Opponent
        # --------------------------------------------

        score += self._opponent_bonus(
            state,
            candidate,
        )

        candidate.score = score

        score += self._strategic_bonus(
    state,
    candidate,
)

    # =====================================================
    # Economy Bonus
    # =====================================================

    def _economy_bonus(
        self,
        state: GameState,
        candidate: ActionCandidate,
    ) -> float:

        task = candidate.task

        if task == "SELL":

            product = candidate.target

            price = state.market.price(product)

            if self.economy.should_sell(
                product,
                price,
            ):
                return 20

            dynamic_score = self.economy.dynamic_market_score(
                state,
                product,
            )

            if dynamic_score > 0:
                return dynamic_score

            return -15

        if task == "EXPAND":

            return self.economy.expansion_roi(
                2000,
                3000,
            )

        if task == "HIRE":

            return self.economy.hire_roi(
                1000,
                1800,
            )

        return 0

    # =====================================================
    # Risk Penalty
    # =====================================================
    def _risk_penalty(
        self,
        state: GameState,
        candidate: ActionCandidate,
    ) -> float:

        task = candidate.task

        # Crop actions
        if task in (
            "HARVEST",
            "FERTILIZE",
        ):

            tile = candidate.target

            if tile.is_plant:

                return self.risk.crop_risk(
                    tile.crop
                )

        # Water directly reduces crop risk.
        # Therefore current crop risk should not
        # be charged as a penalty to WATER.
        if task == "WATER":
            return 0

        # Animal collection
        if task == "COLLECT":

            tile = candidate.target

            if tile.has_animal:

                return self.risk.animal_risk(
                    tile.animal
                )

        # FEED and CARE directly reduce animal risk.
        return 0

    # =====================================================
    # Opponent Bonus
    # =====================================================

    def _opponent_bonus(
        self,
        state: GameState,
        candidate: ActionCandidate,
    ) -> float:

        prediction = self.opponent.predict_next_action(
            state
        )

        if (
            prediction == "EXPAND"
            and
            candidate.task == "EXPAND"
        ):
            return 10

        if (
            prediction == "SELL"
            and
            candidate.task == "SELL"
        ):
            return 5

        return 0


    # =====================================================
    # Fallback Decision
    # =====================================================

    def fallback(
        self,
        state: GameState,
    ) -> ActionCandidate | None:
        """
        Returns a safe fallback action if no valid
        candidate is available.
        """

        tasks = self.task_generator.generate(state)

        if not tasks:
            return None

        candidates = self.scheduler.assign(
            state,
            tasks,
        )

        if not candidates:
            return None

        return candidates[0]

    # =====================================================
    # Diagnostics
    # =====================================================

    def evaluate_all(
        self,
        state: GameState,
    ) -> list[ActionCandidate]:
        """
        Returns every evaluated candidate.
        Useful for debugging and testing.
        """

        tasks = self.task_generator.generate(
            state
        )

        candidates = self.scheduler.assign(
            state,
            tasks,
        )

        results = []

        for candidate in candidates:

            candidate = self.evaluator.evaluate(
                state,
                candidate,
            )

            self._apply_global_adjustments(
                state,
                candidate,
            )

            results.append(candidate)

        results.sort(
            key=lambda c: c.final_score,
            reverse=True,
        )

        return results

    # =====================================================
    # Debug
    # =====================================================

    def print_rankings(
        self,
        state: GameState,
    ) -> None:
        """
        Prints ranked candidate actions.
        """

        candidates = self.evaluate_all(
            state
        )

        print("\n===== Decision Rankings =====")

        for i, candidate in enumerate(
            candidates,
            start=1,
        ):

            print(
                f"{i:02d}. "
                f"{candidate.task:<20}"
                f"Score={candidate.final_score:.2f}"
            )

    # =====================================================
    # Memory Access
    # =====================================================

    def memory_state(self) -> BrainMemory:
        """
        Returns the internal memory object.
        """

        return self.memory

    # =====================================================
    # Reset
    # =====================================================

    def reset(self) -> None:
        """
        Resets the AI memory.
        """

        self.memory.reset()

    # =====================================================
    # Statistics
    # =====================================================

    def statistics(self) -> dict:
        """
        Returns runtime statistics.
        """

        return {

            "turns":

                len(
                    self.memory.action_history
                ),

            "actions":

                len(
                    self.memory.action_history
                ),

            "money_samples":

                len(
                    self.memory.money_history
                ),

            "opponent_samples":

                len(
                    self.memory.opponent_money_history
                ),

            "tracked_products":

                len(
                    self.memory.market_price_history
                ),
        }

    # =====================================================
    # String Representation
    # =====================================================

    def __repr__(self):

        return (
            "DecisionEngine("
            f"history={len(self.memory.action_history)})"
        )


    def _strategic_bonus(
        self,
        state: GameState,
        candidate: ActionCandidate,
    ) -> float:

        recommendation = self.strategy.risk_adjusted_recommendation(
    state
)

        task = candidate.task

        strategic_map = {
            "PRESERVE_CAPITAL": {
                "BUY_PRODUCT": -30,
                "BUY_ANIMAL": -25,
                "BUY_SEED": -10,
                "EXPAND": -40,
                "SELL": 15,
            },

            "EXPAND": {
                "EXPAND": 35,
                "BUY_PRODUCT": -10,
                "BUY_ANIMAL": 10,
                "SELL": 5,
            },

            "GROW": {
                "BUY_SEED": 30,
                "PLANT": 30,
                "BUY_ANIMAL": 5,
                "SELL": 0,
            },

            "BUILD_LIVESTOCK": {
                "BUY_ANIMAL": 35,
                "PLACE": 25,
                "BUY_SEED": 5,
            },

            "PRODUCE": {
                "BUY_SEED": 25,
                "PLANT": 30,
                "PLACE": 15,
            },

            "OPTIMIZE_MARKET": {
                "SELL": 20,
                "BUY_PRODUCT": 15,
            },
        }

        return strategic_map.get(
            recommendation,
            {},
        ).get(task, 0)