"""Creature body model and action loop."""

from __future__ import annotations

from dataclasses import dataclass, field
import math
import random

import numpy as np

from brain.base import Brain
from creature.sensors import sense_world
from world.world import World


@dataclass
class Creature:
    """Single autonomous creature with sensors, body state, and brain."""

    x: float
    y: float
    heading: float
    energy: float
    health: float
    max_speed: float
    rotation_speed: float
    sensor_range: float
    vision_fov: float
    energy_decay: float
    rest_recovery: float
    brain: Brain
    age: int = 0
    food_eaten: int = 0
    alive: bool = True
    last_reward: float = 0.0
    behavior_state: str = "wander"
    activity_trace: list[float] = field(default_factory=list)

    def step(self, world: World, rng: random.Random) -> None:
        """Advance creature by one simulation step."""
        if not self.alive:
            return

        sensory_input = sense_world(
            cx=self.x,
            cy=self.y,
            heading=self.heading,
            energy=self.energy,
            health=self.health,
            sensor_range=self.sensor_range,
            fov=self.vision_fov,
            world=world,
        )
        outputs = self.brain.step(sensory_input, reward=self.last_reward)
        self._apply_actions(outputs, world)
        reward = self._resolve_world_interactions(world)

        self.energy -= self.energy_decay
        self.age += 1

        if self.energy <= 0:
            self.health -= 0.6
        if self.health <= 0:
            self.alive = False

        self.last_reward = reward
        self.activity_trace.append(float(np.mean(np.abs(self.brain.get_activity()))))

    def _apply_actions(self, out: np.ndarray, world: World) -> None:
        move_drive = float(out[0])
        turn_drive = float(out[1])
        eat_drive = float(out[2])
        rest_drive = float(out[3])

        self.heading += turn_drive * self.rotation_speed
        speed = move_drive * self.max_speed

        self.x += math.cos(self.heading) * speed
        self.y += math.sin(self.heading) * speed

        self.behavior_state = "wander"
        if eat_drive > 0.3:
            self.behavior_state = "eat"
        elif rest_drive > 0.3:
            self.behavior_state = "rest"
            self.energy += self.rest_recovery

        if self.x < 0:
            self.x = 0
            self.health -= world.boundary_damage
        elif self.x > world.width:
            self.x = world.width
            self.health -= world.boundary_damage

        if self.y < 0:
            self.y = 0
            self.health -= world.boundary_damage
        elif self.y > world.height:
            self.y = world.height
            self.health -= world.boundary_damage

    def _resolve_world_interactions(self, world: World) -> float:
        reward = 0.01  # living baseline

        for hazard in world.hazards:
            if math.hypot(self.x - hazard.x, self.y - hazard.y) < hazard.radius:
                self.health -= hazard.damage
                reward -= 0.07

        eaten_index = None
        for i, food in enumerate(world.food):
            if math.hypot(self.x - food.x, self.y - food.y) < (food.radius + 7):
                self.energy += food.energy_value
                self.food_eaten += 1
                reward += 0.3
                eaten_index = i
                break

        if eaten_index is not None:
            world.food.pop(eaten_index)

        self.energy = max(0.0, min(130.0, self.energy))
        self.health = max(0.0, min(100.0, self.health))

        reward += (self.energy / 100.0) * 0.005
        return reward
