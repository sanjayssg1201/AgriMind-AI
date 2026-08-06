from dataclasses import dataclass, field


@dataclass
class Town:
    """Represents town demand."""

    requested_items: dict[str, int] = field(default_factory=dict)