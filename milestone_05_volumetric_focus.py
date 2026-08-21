"""Milestone 5: later extension from one focal point to seven anchors.

Do not begin this script until Milestones 1-4 work correctly.
"""

from pathlib import Path

import numpy as np

from beamforming import multi_focus_weights
from channel import field_on_points
from config import CONFIG
from geometry import make_uniform_triangular_tower
from metrics import power_to_db
from plots import plot_power_map


OUTPUT_DIR = Path("outputs")


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    positions, _, _, _ = make_uniform_triangular_tower(
        CONFIG.tower_side_length,
        CONFIG.tower_height,
        CONFIG.num_horizontal,
        CONFIG.num_vertical,
        CONFIG.element_spacing,
    )

    center = np.array([25.0, 0.0, CONFIG.tower_height])
    offsets = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [-1.0, 0.0, 0.0],
            [0.0, 0.5, 0.0],
            [0.0, -0.5, 0.0],
            [0.0, 0.0, 0.5],
            [0.0, 0.0, -0.5],
        ]
    )
    anchors = center + offsets
    coefficients = np.ones(anchors.shape[0], dtype=complex)
    weights = multi_focus_weights(
        anchors,
        coefficients,
        positions,
        CONFIG.wavelength,
    )

    x_values = np.linspace(20.0, 30.0, 221)
    y_values = np.linspace(-3.0, 3.0, 181)
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
    power = (np.abs(field) ** 2).reshape(x_grid.shape)

    plot_power_map(
        x_values,
        y_values,
        power_to_db(power),
        "x (m)",
        "y (m)",
        "Milestone 5: seven-anchor beam, horizontal slice",
        OUTPUT_DIR / "m05_volumetric_focus_slice.png",
        focus_coordinates=(center[0], center[1]),
    )


if __name__ == "__main__":
    main()

