"""Entry point for Brain-sim local-first prototype."""

from __future__ import annotations

import argparse

from simulation.config import load_config
from simulation.runner import SimulationRunner


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Artificial brain simulator prototype")
    parser.add_argument("--config", default="config/default.json", help="Path to JSON config file")
    parser.add_argument("--headless", action="store_true", help="Run without pygame display")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = load_config(args.config)
    if args.headless:
        cfg["headless"] = True
    runner = SimulationRunner(cfg)
    runner.run()


if __name__ == "__main__":
    main()
