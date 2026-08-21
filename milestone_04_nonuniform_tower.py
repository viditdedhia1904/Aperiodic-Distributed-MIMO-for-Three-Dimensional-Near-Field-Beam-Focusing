"""Milestone 4: compare uniform and one non-uniform panel placement.

The non-uniform fractions below are only a test geometry. They are not claimed
to be optimal.
"""

from pathlib import Path

import numpy as np

from beamforming import focus_weights
from channel import field_on_points
from config import CONFIG
from geometry import make_triangular_tower
from metrics import power_to_db, strongest_outside_lobe_db
from plots import plot_geometry, plot_power_map


OUTPUT_DIR = Path("outputs")


def evaluate_layout(name: str, fractions: np.ndarray) -> float:
    positions, panel_ids, _, _ = make_triangular_tower(
        CONFIG.tower_side_length,
        CONFIG.tower_height,
        fractions,
        CONFIG.num_horizontal,
        CONFIG.num_vertical,
        CONFIG.element_spacing,
    )
    plot_geometry(
        positions,
        f"{name} tower geometry",
        OUTPUT_DIR / f"m04_{name}_geometry.png",
        panel_ids,
    )

    focus = np.array([25.0, 0.0, CONFIG.tower_height])
    weights = focus_weights(focus, positions, CONFIG.wavelength)

    x_values = np.linspace(5.0, 40.0, 221)
    y_values = np.linspace(-20.0, 20.0, 241)
    x_grid, y_grid = np.meshgrid(x_values, y_values)
    points = np.column_stack(
        [x_grid.ravel(), y_grid.ravel(), np.full(x_grid.size, CONFIG.tower_height)]
    )
    field = field_on_points(
        points,
        positions,
        weights,
        CONFIG.wavelength,
        chunk_size=CONFIG.chunk_size,
    )
    power = np.abs(field) ** 2
    lobe_db = strongest_outside_lobe_db(power, points, focus, guard_radius=1.5)

    plot_power_map(
        x_values,
        y_values,
        power_to_db(power.reshape(x_grid.shape)),
        "x (m)",
        "y (m)",
        f"Milestone 4: {name} tower",
        OUTPUT_DIR / f"m04_{name}_focus.png",
        focus_coordinates=(focus[0], focus[1]),
    )
    return lobe_db


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    uniform = np.tile([1.0 / 3.0, 2.0 / 3.0], (3, 1))
    nonuniform = np.array(
        [
            [0.28, 0.69],
            [0.35, 0.74],
            [0.22, 0.60],
        ]
    )

    uniform_lobe = evaluate_layout("uniform", uniform)
    nonuniform_lobe = evaluate_layout("nonuniform", nonuniform)
    print(f"Uniform strongest outside value:    {uniform_lobe:.2f} dB")
    print(f"Non-uniform strongest outside value: {nonuniform_lobe:.2f} dB")
    print("These values describe one target and one test grid, not a final conclusion.")


if __name__ == "__main__":
    main()

