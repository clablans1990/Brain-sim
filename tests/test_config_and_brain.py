import numpy as np

from brain.factory import create_brain
from simulation.config import load_config


def test_load_default_config():
    cfg = load_config("config/default.json")
    assert cfg["seed"] == 42
    assert "world" in cfg


def test_brain_factory_threshold_step_shape():
    rng = np.random.default_rng(42)
    brain = create_brain("threshold", 8, 12, 4, 0.01, rng)
    out = brain.step(np.zeros(8, dtype=np.float32), reward=0.0)
    assert out.shape == (4,)
