"""Simple biologically inspired threshold-neuron brain."""

from __future__ import annotations

import numpy as np

from brain.base import Brain


class ThresholdBrain(Brain):
    """Recurrent threshold network with leaky state dynamics."""

    def __init__(self, input_size: int, hidden_size: int, output_size: int, rng: np.random.Generator) -> None:
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        self.w_in = rng.normal(0.0, 0.7, size=(hidden_size, input_size))
        self.w_rec = rng.normal(0.0, 0.2, size=(hidden_size, hidden_size))
        self.w_out = rng.normal(0.0, 0.7, size=(output_size, hidden_size))
        self.threshold = rng.uniform(0.1, 0.5, size=(hidden_size,))
        self.state = np.zeros(hidden_size)

    def step(self, sensory_input: np.ndarray, reward: float = 0.0) -> np.ndarray:
        leak = 0.85
        drive = self.w_in @ sensory_input + self.w_rec @ self.state
        self.state = leak * self.state + (1.0 - leak) * drive

        spikes = (self.state > self.threshold).astype(np.float32)
        outputs = np.tanh(self.w_out @ spikes)

        # Tiny reward-modulated plasticity for Stage 1 exploration.
        if reward != 0.0:
            eta = 0.001
            self.w_out += eta * reward * np.outer(outputs, spikes)

        return outputs

    def get_activity(self) -> np.ndarray:
        return self.state.copy()
