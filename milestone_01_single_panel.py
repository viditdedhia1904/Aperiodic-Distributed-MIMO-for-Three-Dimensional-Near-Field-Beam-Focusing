"""Milestone 1: focus a small panel at a point 20 m away."""

from pathlib import Path

import numpy as np

from beamforming import focus_weights
from channel import field_on_points
from config import CONFIG
from geometry import make_panel
from metrics import power_to_db
from plots import plot_geometry, plot_power_map


OUTPUT_DIR = Path("outputs")


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    positions = make_panel(
        center=[0.0, 0.0, 0.0],
        horizontal_axis=[0.0, 1.0, 0.0],
        vertical_axis=[0.0, 0.0, 1.0],
        num_horizontal=CONFIG.num_horizontal,
        num_vertical=CONFIG.num_vertical,
        spacing=CONFIG.element_spacing,
    )
    plot_geometry(positions, "Small planar array", OUTPUT_DIR / "m01_panel.png")

    focus = np.array([20.0, 0.0, 0.0])
    weights = focus_weights(focus, positions, CONFIG.wavelength)

    range_values = np.linspace(15.0, 25.0, 241)
    lateral_values = np.linspace(-2.0, 2.0, 161)
    range_grid, lateral_grid = np.meshgrid(range_values, lateral_values)
    points = np.column_stack(
        [
            range_grid.ravel(),
            lateral_grid.ravel(),
            np.zeros(range_grid.size),
        ]
    )

    field = field_on_points(
        points,
        positions,
        weights,
        CONFIG.wavelength,
        chunk_size=CONFIG.chunk_size,
    )
    power = (np.abs(field) ** 2).reshape(range_grid.shape)
    power_db = power_to_db(power)

    peak_index = np.unravel_index(np.argmax(power), power.shape)
    peak = (range_grid[peak_index], lateral_grid[peak_index])
    print(f"Requested focus (range, lateral): ({focus[0]:.2f}, {focus[1]:.2f}) m")
    print(f"Grid peak       (range, lateral): ({peak[0]:.2f}, {peak[1]:.2f}) m")

    plot_power_map(
        range_values,
        lateral_values,
        power_db,
        "Range x (m)",
        "Lateral position y (m)",
        "Milestone 1: single-panel near-field focus",
        OUTPUT_DIR / "m01_single_panel_focus.png",
        focus_coordinates=(focus[0], focus[1]),
    )


if __name__ == "__main__":
    main()

