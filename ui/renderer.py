"""Pygame rendering for the simulation."""

from __future__ import annotations

import math

import pygame

from creature.creature import Creature
from world.world import World


class Renderer:
    """Draw world and creature state for interactive runs."""

    def __init__(self, width: int, height: int) -> None:
        pygame.init()
        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Brain-Sim Stage 1")
        self.font = pygame.font.SysFont("consolas", 16)

    def draw(self, world: World, creature: Creature, step: int) -> None:
        night_factor = 1.0 - world.state.light_level
        bg = (int(30 + 70 * (1 - night_factor)), int(40 + 70 * (1 - night_factor)), int(50 + 80 * (1 - night_factor)))
        self.surface.fill(bg)

        for food in world.food:
            pygame.draw.circle(self.surface, (70, 220, 90), (int(food.x), int(food.y)), int(food.radius))

        for hazard in world.hazards:
            pygame.draw.circle(self.surface, (200, 70, 70), (int(hazard.x), int(hazard.y)), int(hazard.radius), 1)

        pygame.draw.circle(self.surface, (70, 130, 255), (int(creature.x), int(creature.y)), 8)
        tip_x = creature.x + 13 * math.cos(creature.heading)
        tip_y = creature.y + 13 * math.sin(creature.heading)
        pygame.draw.line(self.surface, (230, 230, 255), (creature.x, creature.y), (tip_x, tip_y), 2)

        status = (
            f"step={step} energy={creature.energy:.1f} health={creature.health:.1f} "
            f"food={creature.food_eaten} state={creature.behavior_state}"
        )
        text = self.font.render(status, True, (240, 240, 240))
        self.surface.blit(text, (10, 8))

        pygame.display.flip()

    def close(self) -> None:
        pygame.quit()
