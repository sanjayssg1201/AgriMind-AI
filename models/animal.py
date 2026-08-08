"""
models/animal.py

Animal model for AgriMind AI.
"""

from dataclasses import dataclass

from core.constants import AnimalType, BuildingType


@dataclass(slots=True)
class Animal:
    """
    Represents an animal placed inside a Coop or Pasture.
    """

    structure: BuildingType

    animal_type: AnimalType | None

    placed_day: int

    fed_today: bool

    cared_today: bool

    consecutive_unfed: int

    fertilizer_available: bool

    pending_care_bonus: int

    yield_units: int

    # ==================================================
    # Basic Properties
    # ==================================================

    @property
    def exists(self) -> bool:
        return self.animal_type is not None

    @property
    def name(self) -> str | None:
        if self.animal_type is None:
            return None
        return self.animal_type.value

    @property
    def building(self) -> str:
        return self.structure.value

    # ==================================================
    # Daily State
    # ==================================================

    @property
    def needs_feed(self) -> bool:
        return self.exists and not self.fed_today

    @property
    def needs_care(self) -> bool:
        return self.exists and not self.cared_today

    @property
    def is_fed(self) -> bool:
        return self.fed_today

    @property
    def is_cared(self) -> bool:
        return self.cared_today

    # ==================================================
    # Production
    # ==================================================

    @property
    def has_product(self) -> bool:
        return self.yield_units > 0

    @property
    def can_collect_fertilizer(self) -> bool:
        return (
            self.exists
            and
            self.fertilizer_available
        )

    # ==================================================
    # Health
    # ==================================================

    @property
    def is_starving(self) -> bool:
        return self.consecutive_unfed >= 1

    @property
    def escaped(self) -> bool:
        """
        Conservative helper.
        Escape rules remain enforced by the game engine.
        """
        return (
            self.exists
            and
            self.consecutive_unfed >= 2
        )

    @property
    def health(self) -> float:
        """
        Returns animal health between 0 and 1.
        """

        if self.consecutive_unfed == 0:
            return 1.0

        return max(
            0.0,
            1.0 - (self.consecutive_unfed / 5)
        )

    # ==================================================
    # AI Score
    # ==================================================

    @property
    def production_score(self) -> float:
        """
        Heuristic used by planners.
        """

        score = float(self.yield_units)

        if self.pending_care_bonus > 0:
            score += self.pending_care_bonus

        if self.fertilizer_available:
            score += 1.5

        return score

    # ==================================================
    # Debug
    # ==================================================

    def __repr__(self):

        if not self.exists:
            return (
                f"{self.structure.value}(Empty)"
            )

        return (
            f"Animal("
            f"{self.animal_type.value}, "
            f"yield={self.yield_units}, "
            f"fed={self.fed_today}, "
            f"care={self.cared_today})"
        )
    