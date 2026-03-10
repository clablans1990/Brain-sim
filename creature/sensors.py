"""Sensor calculations for creature-body interaction with the world."""

from __future__ import annotations

import math
import numpy as np

from world.world import World


def _distance_and_angle(cx: float, cy: float, tx: float, ty: float, heading: float) -> tuple[float, float]:
    dx = tx - cx
    dy = ty - cy
    distance = math.hypot(dx, dy)
    angle = math.atan2(dy, dx) - heading
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle < -math.pi:
        angle += 2 * math.pi
    return distance, angle


def sense_world(cx: float, cy: float, heading: float, energy: float, health: float, sensor_range: float, fov: float, world: World) -> np.ndarray:
    """Create compact sensory vector from local environment and internal state."""
    nearest_food = 1.0
    food_dir = 0.0
    for food in world.food:
        dist, ang = _distance_and_angle(cx, cy, food.x, food.y, heading)
        if dist <= sensor_range and abs(ang) <= fov / 2:
            proximity = dist / sensor_range
            if proximity < nearest_food:
                nearest_food = proximity
                food_dir = ang / (fov / 2)

    nearest_hazard = 1.0
    hazard_dir = 0.0
    for hazard in world.hazards:
        dist, ang = _distance_and_angle(cx, cy, hazard.x, hazard.y, heading)
        if dist <= sensor_range and abs(ang) <= fov / 2:
            proximity = dist / sensor_range
            if proximity < nearest_hazard:
                nearest_hazard = proximity
                hazard_dir = ang / (fov / 2)

    boundary_x = min(cx / world.width, (world.width - cx) / world.width)
    boundary_y = min(cy / world.height, (world.height - cy) / world.height)
    boundary_pressure = 1.0 - max(0.0, min(boundary_x, boundary_y)) * 2.0

    hunger = 1.0 - max(0.0, min(energy / 100.0, 1.0))
    injury = 1.0 - max(0.0, min(health / 100.0, 1.0))

    return np.array(
        [
            1.0 - nearest_food,
            food_dir,
            1.0 - nearest_hazard,
            hazard_dir,
            boundary_pressure,
            hunger,
            injury,
            world.state.light_level,
        ],
        dtype=np.float32,
    )
