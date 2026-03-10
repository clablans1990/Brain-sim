"""Runtime logging and artifact saving utilities."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt


class RunLogger:
    """Collect scalar metrics and persist them for later analysis."""

    def __init__(self, run_name: str) -> None:
        self.run_name = run_name
        self.rows: list[dict[str, Any]] = []
        self.output_dir = Path("data") / run_name
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def log(self, step: int, energy: float, health: float, food_eaten: int, reward: float, brain_activity: float) -> None:
        self.rows.append(
            {
                "step": step,
                "energy": energy,
                "health": health,
                "food_eaten": food_eaten,
                "reward": reward,
                "brain_activity": brain_activity,
            }
        )

    def save(self) -> None:
        if not self.rows:
            return

        csv_path = self.output_dir / "run_metrics.csv"
        with csv_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(self.rows[0].keys()))
            writer.writeheader()
            writer.writerows(self.rows)

        self._save_plot()

    def _save_plot(self) -> None:
        steps = [r["step"] for r in self.rows]
        energy = [r["energy"] for r in self.rows]
        health = [r["health"] for r in self.rows]
        brain_activity = [r["brain_activity"] for r in self.rows]

        fig, ax = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
        ax[0].plot(steps, energy, label="Energy")
        ax[0].plot(steps, health, label="Health")
        ax[0].legend()
        ax[0].set_ylabel("Body State")

        ax[1].plot(steps, brain_activity, label="Brain Activity", color="purple")
        ax[1].set_ylabel("Activity")
        ax[1].set_xlabel("Step")

        fig.tight_layout()
        fig.savefig(self.output_dir / "diagnostics.png")
        plt.close(fig)
