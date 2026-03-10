"""World entities used in the simulation."""

from dataclasses import dataclass


@dataclass
class Food:
    """A consumable food pellet that restores energy."""

    x: float
    y: float
    radius: float
    energy_value: float = 18.0


@dataclass
class Hazard:
    """A hazard area that damages creatures on contact."""

    x: float
    y: float
    radius: float
    damage: float = 1.3
