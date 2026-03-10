# Brain-sim (Stage 1 Prototype)

A local-first Python sandbox for experimenting with biologically inspired digital organisms.

## What is implemented now (Stage 1)

- Modular project structure for world, creature body, brain, UI, simulation runtime, and analysis outputs.
- 2D world with boundaries, food resources, hazards, and a simple day/night environmental state.
- One creature with body state (`position`, `heading`, `energy`, `health`, `age`) and simple sensors:
  - local food direction/proximity
  - local hazard direction/proximity
  - boundary pressure
  - internal hunger/injury
  - ambient light level
- Action loop with motor outputs:
  - move forward/backward
  - rotate left/right
  - eat by contact with food
  - rest to recover energy
- Two brain modes behind a clean interface:
  - `threshold`: hand-built recurrent threshold neuron network with leaky dynamics
  - `learnable`: recurrent tanh network with reward-modulated Hebbian-style updates
- Reproducibility via random seed in config.
- Data logging to CSV + matplotlib diagnostics plot.
- Basic unit tests.

## Planned stages

- **Stage 2:** Rich debug overlays (sensor rays, behavior labels, brain activity panels, toggle controls).
- **Stage 3:** Stronger in-lifetime learning/reward shaping and experiment scripts.
- **Stage 4:** Multi-creature populations + optional evolutionary loop.
- **Stage 5:** Architecture cleanup, replay mode, brain import/export, and parameter sweeps.

## Project layout

- `main.py` - entrypoint
- `config/` - JSON configuration
- `simulation/` - config loader and runtime loop
- `world/` - world/entities/environment state
- `creature/` - body + sensors
- `brain/` - modular brain implementations
- `ui/` - pygame rendering
- `analysis/` - logging and plots
- `data/` - generated run outputs
- `tests/` - basic tests

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

## Run

Interactive pygame run:

```bash
python main.py --config config/default.json
```

Headless run (fast, no window):

```bash
python main.py --config config/default.json --headless
```

## Tuning parameters

Edit `config/default.json`:

- `brain.mode`: `threshold` or `learnable`
- `simulation.max_steps`: run length
- `world.food_count` / `world.hazard_count`: environment pressure
- `creature.*`: movement, sensor, and metabolism dynamics
- `seed`: deterministic reproducibility

## Outputs

Each run writes to `data/<run_name>/`:

- `run_metrics.csv`
- `diagnostics.png`

## Example experiments

1. Compare brain modes by switching `brain.mode` and keeping the same seed.
2. Increase `hazard_count` to pressure avoidance behavior.
3. Reduce `food_count` and inspect energy survival curves.

