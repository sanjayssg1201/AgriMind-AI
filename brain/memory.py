"""
brain/memory.py

Memory and learning system for AgriMind AI.

Stores:
- observed game states
- selected actions
- action scores
- outcomes
- action/reward experiences
- historical market prices
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class BrainMemory:
    """
    Persistent memory used by the AgriMind brain.

    Stores observations and previous decisions so that
    economy, strategy, risk, and planning components can
    use historical information.
    """

    # ==================================================
    # Core Memory
    # ==================================================

    states: list[Any] = field(
        default_factory=list
    )

    actions: list[Any] = field(
        default_factory=list
    )

    outcomes: list[Any] = field(
        default_factory=list
    )

    # ==================================================
    # Experience Learning
    # ==================================================

    experience_history: list[dict[str, Any]] = field(
        default_factory=list
    )

    # ==================================================
    # Market History
    # ==================================================

    price_history: dict[str, list[float]] = field(
        default_factory=dict
    )

    # ==================================================
    # Configuration
    # ==================================================

    max_history: int = 1000

    # ==================================================
    # State Memory
    # ==================================================

    def update(
        self,
        state: Any,
    ) -> None:
        """
        Store the latest game state.

        Also records observed market prices so that
        historical market signals can be calculated later.
        """

        self.states.append(state)

        if len(self.states) > self.max_history:
            self.states.pop(0)

        # ----------------------------------------------
        # Record market prices
        # ----------------------------------------------

        market = getattr(
            state,
            "market",
            None,
        )

        if market is None:
            return

        prices = getattr(
            market,
            "prices",
            None,
        )

        if not isinstance(
            prices,
            dict,
        ):
            return

        for product, price in prices.items():

            try:

                value = float(price)

            except (
                TypeError,
                ValueError,
            ):

                continue

            history = self.price_history.setdefault(
                product,
                [],
            )

            history.append(value)

            if len(history) > self.max_history:
                history.pop(0)


    def price_trend(
        self,
        product: str,
    ) -> float:
        """
        Return the recent price trend for a product.

        Positive  -> price is increasing
        Negative  -> price is decreasing
        Zero      -> insufficient history or no movement
        """

        history = self.price_history.get(
            product,
            [],
        )

        if len(history) < 2:
            return 0.0

        previous = history[-2]
        current = history[-1]

        if previous == 0:
            return 0.0

        return (
            (current - previous)
            / previous
        ) * 100.0

    # ==================================================
    # Action Memory
    # ==================================================

    def remember_action(
        self,
        action: Any,
        score: float = 0.0,
    ) -> None:
        """
        Store an action and its evaluated score.
        """

        self.actions.append(
            {
                "action": action,
                "score": float(score),
            }
        )

        if len(self.actions) > self.max_history:
            self.actions.pop(0)

    # ==================================================
    # Outcome Memory
    # ==================================================

    def remember_outcome(
        self,
        outcome: Any,
    ) -> None:
        """
        Store an observed outcome.
        """

        self.outcomes.append(
            outcome
        )

        if len(self.outcomes) > self.max_history:
            self.outcomes.pop(0)

    # ==================================================
    # Experience Learning
    # ==================================================

    def remember_experience(
        self,
        action: Any,
        reward: float,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """
        Store one action/reward experience.

        Parameters
        ----------
        action:
            Action that was performed.

        reward:
            Reward received after the action.

        metadata:
            Optional contextual information about the
            experience.
        """

        experience = {
            "action": action,
            "reward": float(reward),
            "metadata": metadata or {},
        }

        self.experience_history.append(
            experience
        )

        if (
            len(self.experience_history)
            > self.max_history
        ):
            self.experience_history.pop(0)

    # ==================================================
    # Experience Queries
    # ==================================================

    def action_experience_count(
        self,
        action: Any,
    ) -> int:
        """
        Return the number of recorded experiences
        for an action.
        """

        return sum(
            1
            for experience
            in self.experience_history
            if experience["action"] == action
        )

    def action_average_reward(
        self,
        action: Any,
    ) -> float:
        """
        Return the average historical reward for
        an action.

        Unknown actions return 0.0.
        """

        rewards = [
            experience["reward"]
            for experience
            in self.experience_history
            if experience["action"] == action
        ]

        if not rewards:
            return 0.0

        return sum(rewards) / len(rewards)

    def action_reward(
        self,
        action: Any,
    ) -> float:
        """
        Return the most recent recorded reward
        for an action.

        Unknown actions return 0.0.
        """

        for experience in reversed(
            self.experience_history
        ):

            if experience["action"] == action:

                return float(
                    experience["reward"]
                )

        return 0.0

    # ==================================================
    # Historical Market Prices
    # ==================================================

    def historical_average_price(
        self,
        product: str,
    ) -> float:
        """
        Return the historical average market price
        observed for a product.

        Unknown products return 0.0.
        """

        history = self.price_history.get(
            product,
            [],
        )

        if not history:
            return 0.0

        return sum(history) / len(history)

    # ==================================================
    # Existing Score Learning
    # ==================================================

    def action_average_score(
        self,
        action: Any,
    ) -> float:
        """
        Return the average score previously assigned
        to an action.

        Unknown actions return 0.0.
        """

        scores = [
            entry["score"]
            for entry in self.actions
            if (
                isinstance(
                    entry,
                    dict,
                )
                and entry.get("action") == action
            )
        ]

        if not scores:
            return 0.0

        return sum(scores) / len(scores)

    # ==================================================
    # Memory Statistics
    # ==================================================

    @property
    def state_count(self) -> int:
        return len(self.states)

    @property
    def action_count(self) -> int:
        return len(self.actions)

    @property
    def outcome_count(self) -> int:
        return len(self.outcomes)

    @property
    def experience_count(self) -> int:
        return len(
            self.experience_history
        )

    # ==================================================
    # Reset
    # ==================================================

    def reset(self) -> None:
        """
        Clear all stored memory.
        """

        self.states.clear()

        self.actions.clear()

        self.outcomes.clear()

        self.experience_history.clear()

        self.price_history.clear()

    # ==================================================
    # Debug
    # ==================================================

    def __repr__(self) -> str:

        return (
            "BrainMemory("
            f"states={self.state_count}, "
            f"actions={self.action_count}, "
            f"outcomes={self.outcome_count}, "
            f"experiences={self.experience_count}"
            ")"
        )

    def record_decision_outcome(
        self,
        action_type: str,
        expected_reward: float,
        actual_reward: float,
    ) -> None:
        """Record the outcome of a completed decision."""

        if not hasattr(self, "decision_outcomes"):
            self.decision_outcomes = []

        self.decision_outcomes.append(
            {
                "action_type": action_type,
                "expected_reward": expected_reward,
                "actual_reward": actual_reward,
                "error": actual_reward - expected_reward,
            }
        )


    def strategy_success_rate(
        self,
        action_type: str,
    ) -> float:
        """Return the historical success rate for an action type."""

        outcomes = getattr(self, "decision_outcomes", [])

        matching = [
            outcome
            for outcome in outcomes
            if outcome["action_type"] == action_type
        ]

        if not matching:
            return 0.5

        successful = sum(
            1
            for outcome in matching
            if outcome["actual_reward"] >= outcome["expected_reward"]
        )

        return successful / len(matching)