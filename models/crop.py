"""
models/crop.py

Crop model for AgriMind AI.
"""

from dataclasses import dataclass

from core.constants import CropType


@dataclass(slots=True)
class Crop:
    """
    Represents a crop growing on a farm tile.
    """

    crop_type: CropType

    planted_day: int

    watered_today: bool

    consecutive_unwatered: int

    yield_units: int

    fertilized_until_day: int

    max_lifespan_step: int

    # ==================================================
    # AI Helpers
    # ==================================================

    @property
    def name(self) -> str:
        return self.crop_type.value

    @property
    def needs_water(self) -> bool:
        return not self.watered_today

    @property
    def is_watered(self) -> bool:
        return self.watered_today

    @property
    def is_fertilized(self) -> bool:
        return self.fertilized_until_day >= 0

    @property
    def can_harvest(self) -> bool:
        return self.yield_units > 0

    @property
    def is_dying(self) -> bool:
        return self.consecutive_unwatered >= 1

    @property
    def remaining_life(self) -> int:
        return max(
            0,
            self.max_lifespan_step - self.consecutive_unwatered
        )

    @property
    def health(self) -> float:
        """
        Returns crop health between 0 and 1.
        """

        if self.max_lifespan_step <= 0:
            return 1.0

        return max(
            0.0,
            1.0 - (
                self.consecutive_unwatered /
                self.max_lifespan_step
            )
        )

    # ==================================================
    # Debug
    # ==================================================

    def __repr__(self):

        return (
            f"Crop("
            f"{self.crop_type.value}, "
            f"yield={self.yield_units}, "
            f"watered={self.watered_today})"
        )