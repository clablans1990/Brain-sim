"""2D world model with resources and environmental state."""

from __future__ import annotations

from dataclasses import dataclass
import math
import random

from world.entities import Food, Hazard


@dataclass
class EnvironmentState:
    """Simple cyclic day/night state."""

    phase: float
    light_level: float


class World:
    """Container for map dimensions and static entities."""

    def __init__(self, cfg: dict, rng: random.Random) -> None:
        self.width = cfg["width"]
        self.height = cfg["height"]
        self.food_count = cfg["food_count"]
        self.hazard_count = cfg["hazard_count"]
        self.food_radius = cfg["food_radius"]
        self.hazard_radius = cfg["hazard_radius"]
        self.boundary_damage = cfg["boundary_damage"]
        self.rng = rng

        self.food: list[Food] = []
        self.hazards: list[Hazard] = []
        self.state = EnvironmentState(phase=0.0, light_level=1.0)
        self._spawn_entities()

    def _spawn_entities(self) -> None:
        self.food = [
            Food(
                x=self.rng.uniform(20, self.width - 20),
                y=self.rng.uniform(20, self.height - 20),
                radius=self.food_radius,
            )
            for _ in range(self.food_count)
        ]

        self.hazards = [
            Hazard(
                x=self.rng.uniform(20, self.width - 20),
                y=self.rng.uniform(20, self.height - 20),
                radius=self.hazard_radius,
            )
            for _ in range(self.hazard_count)
        ]

    def respawn_food(self) -> None:
        """Maintain a stable number of resources in world."""
        while len(self.food) < self.food_count:
            self.food.append(
                Food(
                    x=self.rng.uniform(20, self.width - 20),
                    y=self.rng.uniform(20, self.height - 20),
                    radius=self.food_radius,
                )
            )

    def update_environment(self, step: int, day_length_steps: int) -> None:
        """Update day-night cycle based on the current step."""
        phase = (step % day_length_steps) / day_length_steps
        # Light oscillates between 0.25 and 1.0
        light = 0.625 + 0.375 * math.sin(2 * math.pi * phase)
        self.state = EnvironmentState(phase=phase, light_level=light)
