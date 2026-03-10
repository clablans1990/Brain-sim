"""Factory for creating brain implementations."""

from __future__ import annotations

import numpy as np

from brain.base import Brain
from brain.learnable_brain import LearnableBrain
from brain.threshold_brain import ThresholdBrain


def create_brain(mode: str, input_size: int, hidden_size: int, output_size: int, learning_rate: float, rng: np.random.Generator) -> Brain:
    """Create a brain by mode name."""
    if mode == "threshold":
        return ThresholdBrain(input_size, hidden_size, output_size, rng)
    if mode == "learnable":
        return LearnableBrain(input_size, hidden_size, output_size, learning_rate, rng)
    raise ValueError(f"Unknown brain mode: {mode}")
