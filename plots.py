"""Reusable plotting helpers.

This file is supplied almost complete so that the student can focus first on
the physics and numerical calculations.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import ArrayLike


def plot_geometry(
    element_positions: ArrayLike,
    title: str,
    output_file: str | Path,
    panel_ids: ArrayLike | None = None,
) -> None:
    positions = np.asarray(element_positions)
    figure = plt.figure(figsize=(7, 6))
    axis = figure.add_subplot(111, projection="3d")
    if panel_ids is None:
        axis.scatter(
            positions[:, 0],
            positions[:, 1],
            positions[:, 2],
            s=5,
        )
    else:
        axis.scatter(
            positions[:, 0],
            positions[:, 1],
            positions[:, 2],
            c=np.asarray(panel_ids),
            s=5,
            cmap="tab10",
        )
    axis.set_xlabel("x (m)")
    axis.set_ylabel("y (m)")
    axis.set_zlabel("z (m)")
    axis.set_title(title)
    figure.tight_layout()
    figure.savefig(output_file, dpi=200)
    plt.close(figure)


def plot_power_map(
    horizontal_values: ArrayLike,
    vertical_values: ArrayLike,
    power_db: ArrayLike,
    horizontal_label: str,
    vertical_label: str,
    title: str,
    output_file: str | Path,
    focus_coordinates: tuple[float, float] | None = None,
    color_limits: tuple[float, float] = (-30.0, 0.0),
) -> None:
    horizontal_values = np.asarray(horizontal_values)
    vertical_values = np.asarray(vertical_values)
    power_db = np.asarray(power_db)

    figure, axis = plt.subplots(figsize=(7.5, 5.5))
    image = axis.pcolormesh(
        horizontal_values,
        vertical_values,
        power_db,
        shading="auto",
        cmap="turbo",
        vmin=color_limits[0],
        vmax=color_limits[1],
    )
    if focus_coordinates is not None:
        axis.plot(focus_coordinates[0], focus_coordinates[1], "wx", ms=8, mew=2)
    axis.set_xlabel(horizontal_label)
    axis.set_ylabel(vertical_label)
    axis.set_title(title)
    figure.colorbar(image, ax=axis, label="Normalized power (dB)")
    figure.tight_layout()
    figure.savefig(output_file, dpi=200)
    plt.close(figure)


def plot_profile(
    coordinate: ArrayLike,
    power_db: ArrayLike,
    coordinate_label: str,
    title: str,
    output_file: str | Path,
) -> None:
    figure, axis = plt.subplots(figsize=(7, 4))
    axis.plot(coordinate, power_db, lw=2)
    axis.axhline(-3.0, color="black", ls="--", lw=1, label="-3 dB")
    axis.axhline(-10.0, color="gray", ls=":", lw=1, label="-10 dB")
    axis.set_xlabel(coordinate_label)
    axis.set_ylabel("Normalized power (dB)")
    axis.set_ylim(-40.0, 1.0)
    axis.grid(True, alpha=0.3)
    axis.legend()
    axis.set_title(title)
    figure.tight_layout()
    figure.savefig(output_file, dpi=200)
    plt.close(figure)
