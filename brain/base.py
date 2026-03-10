"""Base classes for artificial brain modules."""

from __future__ import annotations

from abc import ABC, abstractmethod
import numpy as np


class Brain(ABC):
    """Common interface for all brain implementations."""

    @abstractmethod
    def step(self, sensory_input: np.ndarray, reward: float = 0.0) -> np.ndarray:
        """Run one simulation step and return motor outputs."""

    @abstractmethod
    def get_activity(self) -> np.ndarray:
        """Return activity vector for visualization/debugging."""
