"""Learnable brain variant using simple predictive updates."""

from __future__ import annotations

import numpy as np

from brain.base import Brain


class LearnableBrain(Brain):
    """Small recurrent tanh network with reward-modulated Hebbian updates."""

    def __init__(self, input_size: int, hidden_size: int, output_size: int, learning_rate: float, rng: np.random.Generator) -> None:
        self.lr = learning_rate
        self.w_in = rng.normal(0.0, 0.5, size=(hidden_size, input_size))
        self.w_rec = rng.normal(0.0, 0.1, size=(hidden_size, hidden_size))
        self.w_out = rng.normal(0.0, 0.5, size=(output_size, hidden_size))
        self.hidden = np.zeros(hidden_size)

    def step(self, sensory_input: np.ndarray, reward: float = 0.0) -> np.ndarray:
        prev_hidden = self.hidden.copy()
        self.hidden = np.tanh(self.w_in @ sensory_input + self.w_rec @ self.hidden)
        out = np.tanh(self.w_out @ self.hidden)

        if reward != 0.0:
            self.w_out += self.lr * reward * np.outer(out, self.hidden)
            self.w_rec += self.lr * reward * np.outer(self.hidden, prev_hidden)

        return out

    def get_activity(self) -> np.ndarray:
        return self.hidden.copy()
