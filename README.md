# Distributed MIMO Near-Field Focusing: Student Starter Code

> **Release check:** This is `TODO-restored-v3`. Before any student work,
> `python check_progress.py` must stop at Task 1 with `[INCOMPLETE]`.
> See `VERSION.txt` if Tasks 1-4 are already passing.

This repository is a starting structure for your undergraduate research
project. It is intentionally incomplete. Search for `TODO` in the Python files
and complete the marked parts one at a time.

Do not try to complete every file at once. Follow this order:

1. `geometry.py`: create one panel.
2. `channel.py`: calculate distances and spherical-wave phases.
3. `beamforming.py`: calculate point-focusing weights.
4. Run `milestone_01_single_panel.py`.
5. Run `milestone_02_separated_panels.py`.
6. Complete the triangular-tower part of `geometry.py`.
7. Run `milestone_03_uniform_tower.py`.
8. Complete the important functions in `metrics.py`.
9. Run `milestone_04_nonuniform_tower.py`.
10. Only after the above steps work, attempt
   `milestone_05_volumetric_focus.py`.

## Installation

Create a virtual environment and install the packages in `requirements.txt`.

Windows PowerShell:

```text
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Linux/macOS:

```text
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Check your progress

After completing a few functions, run:

```text
python check_progress.py
```

The program will stop at the first unfinished stage and tell you which file to
work on next.

## Project files

| File | Purpose |
|---|---|
| `config.py` | Common frequency, array and plotting parameters. |
| `geometry.py` | Antenna-panel and triangular-tower coordinates. |
| `channel.py` | Exact distances and spherical-wave propagation. |
| `beamforming.py` | Point-focus and later multi-focus weights. |
| `metrics.py` | dB normalization, widths and grating-lobe measurements. |
| `plots.py` | Reusable plotting functions. This file is mostly complete. |
| `check_progress.py` | Small numerical checks for your functions. |
| `milestone_01_...py` | First single-panel focusing experiment. |
| `milestone_02_...py` | Experiment with separated panels. |
| `milestone_03_...py` | Uniform nine-panel triangular tower. |
| `milestone_04_...py` | Uniform versus non-uniform tower. |
| `milestone_05_...py` | Later extension from a point to a small volume. |

## Rules for the code

- Use metres for every distance.
- Use radians for every phase.
- Keep array coordinates in NumPy arrays of shape `(number_of_elements, 3)`.
- Keep observation points in arrays of shape `(number_of_points, 3)`.
- Do not write a Python loop over antenna elements. Use NumPy broadcasting.
- Process a large observation grid in chunks.
- Use the same total weight norm in every beam comparison.
- Save each final figure using the script that generated it.
- Set a random seed before random placement experiments.

The first scientific goal is not optimization. It is to obtain a correct,
reproducible spatial power map whose maximum is close to the requested focal
point.
