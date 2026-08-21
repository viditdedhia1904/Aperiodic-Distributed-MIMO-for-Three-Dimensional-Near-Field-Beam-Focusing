"""Milestone 2: repeat point focusing with three separated panels."""

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

    panel_centers = [
        [0.0, -2.0, 0.0],
        [0.0, 0.0, 0.0],
        [0.0, 2.0, 0.0],
    ]
    panels = [
        make_panel(
            center=center,
            horizontal_axis=[0.0, 1.0, 0.0],
            vertical_axis=[0.0, 0.0, 1.0],
            num_horizontal=CONFIG.num_horizontal,
            num_vertical=CONFIG.num_vertical,
            spacing=CONFIG.element_spacing,
        )
        for center in panel_centers
    ]
    positions = np.vstack(panels)
    panel_ids = np.repeat(np.arange(3), panels[0].shape[0])
    plot_geometry(
        positions,
        "Three separated panels",
        OUTPUT_DIR / "m02_geometry.png",
        panel_ids,
    )

    focus = np.array([20.0, 0.0, 0.0])
    weights = focus_weights(focus, positions, CONFIG.wavelength)

    range_values = np.linspace(15.0, 25.0, 241)
    lateral_values = np.linspace(-5.0, 5.0, 241)
    range_grid, lateral_grid = np.meshgrid(range_values, lateral_values)
    points = np.column_stack(
        [range_grid.ravel(), lateral_grid.ravel(), np.zeros(range_grid.size)]
    )
    field = field_on_points(
        points,
        positions,
        weights,
        CONFIG.wavelength,
        chunk_size=CONFIG.chunk_size,
    )
    power = (np.abs(field) ** 2).reshape(range_grid.shape)

    plot_power_map(
        range_values,
        lateral_values,
        power_to_db(power),
        "Range x (m)",
        "Lateral position y (m)",
        "Milestone 2: three separated panels",
        OUTPUT_DIR / "m02_separated_panels_focus.png",
        focus_coordinates=(focus[0], focus[1]),
    )


if __name__ == "__main__":
    main()

