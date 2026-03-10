"""Simulation runtime loop."""

from __future__ import annotations

import random

import numpy as np
import pygame

from analysis.logger import RunLogger
from brain.factory import create_brain
from creature.creature import Creature
from ui.renderer import Renderer
from world.world import World


class SimulationRunner:
    """Coordinates world updates, creature control, rendering, and logging."""

    def __init__(self, config: dict) -> None:
        self.config = config
        self.seed = config["seed"]
        self.rng = random.Random(self.seed)
        self.np_rng = np.random.default_rng(self.seed)

        self.sim_cfg = config["simulation"]
        self.world = World(config["world"], self.rng)

        input_size = 8
        output_size = 4
        brain_cfg = config["brain"]
        brain = create_brain(
            mode=brain_cfg["mode"],
            input_size=input_size,
            hidden_size=brain_cfg["hidden_size"],
            output_size=output_size,
            learning_rate=brain_cfg["learning_rate"],
            rng=self.np_rng,
        )

        creature_cfg = config["creature"]
        self.creature = Creature(
            x=self.world.width / 2,
            y=self.world.height / 2,
            heading=self.rng.uniform(-3.14, 3.14),
            energy=creature_cfg["start_energy"],
            health=creature_cfg["start_health"],
            max_speed=creature_cfg["max_speed"],
            rotation_speed=creature_cfg["rotation_speed"],
            sensor_range=creature_cfg["sensor_range"],
            vision_fov=creature_cfg["vision_fov"],
            energy_decay=creature_cfg["energy_decay"],
            rest_recovery=creature_cfg["rest_recovery"],
            brain=brain,
        )

        run_name = config["logging"]["run_name"]
        self.logger = RunLogger(run_name)
        self.renderer = None if config.get("headless", False) else Renderer(self.world.width, self.world.height)

    def run(self) -> None:
        """Execute full simulation loop."""
        step = 0
        running = True
        clock = pygame.time.Clock()

        while running and step < self.sim_cfg["max_steps"] and self.creature.alive:
            self.world.update_environment(step, self.sim_cfg["day_length_steps"])
            self.creature.step(self.world, self.rng)
            self.world.respawn_food()

            self.logger.log(
                step=step,
                energy=self.creature.energy,
                health=self.creature.health,
                food_eaten=self.creature.food_eaten,
                reward=self.creature.last_reward,
                brain_activity=float(np.mean(np.abs(self.creature.brain.get_activity()))),
            )

            if self.renderer is not None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                self.renderer.draw(self.world, self.creature, step)
                clock.tick(int(self.sim_cfg["fps"] * self.sim_cfg["sim_speed"]))

            step += 1

        self.logger.save()
        if self.renderer is not None:
            self.renderer.close()
