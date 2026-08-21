"""Milestone 3: simulate the uniform nine-panel triangular tower."""

from pathlib import Path

import numpy as np

from beamforming import focus_weights
from channel import field_on_points
from config import CONFIG
from geometry import make_uniform_triangular_tower
from metrics import power_to_db
from plots import plot_geometry, plot_power_map


OUTPUT_DIR = Path("outputs")


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    positions, panel_ids, _, _ = make_uniform_triangular_tower(
        side_length=CONFIG.tower_side_length,
        height=CONFIG.tower_height,
        num_horizontal=CONFIG.num_horizontal,
        num_vertical=CONFIG.num_vertical,
        spacing=CONFIG.element_spacing,
    )
    plot_geometry(
        positions,
        "Uniform nine-panel triangular tower",
        OUTPUT_DIR / "m03_uniform_tower_geometry.png",
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
    power = (np.abs(field) ** 2).reshape(x_grid.shape)

    plot_power_map(
        x_values,
        y_values,
        power_to_db(power),
        "x (m)",
        "y (m)",
        "Milestone 3: uniform distributed tower",
        OUTPUT_DIR / "m03_uniform_tower_focus.png",
        focus_coordinates=(focus[0], focus[1]),
    )


if __name__ == "__main__":
    main()

