"""Functions for creating antenna coordinates.

Coordinate convention used by the milestone scripts:

- x: range direction for the first single-panel example;
- y: horizontal/lateral direction;
- z: vertical direction.

Every returned element-position array must have shape (M, 3).
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray


FloatArray = NDArray[np.float64]


def _unit(vector: ArrayLike) -> FloatArray:
    """Return a unit-length copy of a three-dimensional vector."""
    vector = np.asarray(vector, dtype=float)
    if vector.shape != (3,):
        raise ValueError("A direction vector must have shape (3,).")
    norm = np.linalg.norm(vector)
    if norm == 0:
        raise ValueError("A direction vector cannot be zero.")
    return vector / norm


def make_panel(
    center: ArrayLike,
    horizontal_axis: ArrayLike,
    vertical_axis: ArrayLike,
    num_horizontal: int,
    num_vertical: int,
    spacing: float,
) -> FloatArray:
    """Create element positions for a single planar panel."""
    norm_horizontal_axis = _unit(horizontal_axis)
    norm_vertical_axis = _unit(vertical_axis)
    if abs(np.dot(norm_horizontal_axis, norm_vertical_axis)) > 1.0e-10:
        raise ValueError("The horizontal and vertical axis must be perpendicular.")
    h_offsets = (np.arange(num_horizontal) - (num_horizontal - 1) / 2) * spacing
    v_offsets = (np.arange(num_vertical) - (num_vertical - 1) / 2) * spacing
    H, V = np.meshgrid(h_offsets, v_offsets)
    center_arr = np.asarray(center, dtype=float)
    H_exp = H[..., np.newaxis]
    V_exp = V[..., np.newaxis]
    positions = center_arr + (H_exp * norm_horizontal_axis) + (V_exp * norm_vertical_axis)
    return positions.reshape(-1, 3)


def triangle_vertices(side_length: float, height: float) -> FloatArray:
    """Return the three vertices of an equilateral triangle.

    The triangle is centred around the z-axis. Use circumradius
    R = side_length / sqrt(3) and angles pi/2, 7*pi/6 and 11*pi/6.
    The output must have shape (3, 3).
    """
    radius = side_length / np.sqrt(3)
    angles = np.array([np.pi / 2, 7 * np.pi / 6, 11 * np.pi / 6])
    x = radius * np.cos(angles)
    y = radius * np.sin(angles)
    z = np.full(3, height)
    vertices = np.column_stack((x, y, z))
    return vertices


def panel_axes_from_boresight(boresight: ArrayLike) -> tuple[FloatArray, FloatArray]:
    """Return horizontal and vertical axes for a vertical panel.

    This helper is already complete. The boresight should be horizontal.
    """
    normal = _unit(boresight)
    vertical = np.array([0.0, 0.0, 1.0])
    if abs(np.dot(normal, vertical)) > 1.0e-10:
        raise ValueError("This starter code expects a horizontal boresight.")
    horizontal = _unit(np.cross(vertical, normal))
    return horizontal, vertical


def make_triangular_tower(
    side_length: float,
    height: float,
    side_fractions: ArrayLike,
    num_horizontal: int,
    num_vertical: int,
    spacing: float,
) -> tuple[FloatArray, NDArray[np.int64], FloatArray, FloatArray]:
    """Create three vertex panels and two panels on each triangle side.

    Parameters
    ----------
    side_fractions:
        Array of shape (3, 2). Row s contains the two fractions along side s.
        Uniform placement uses [1/3, 2/3] on all three sides.

    Returns
    -------
    element_positions:
        Shape (M, 3).
    panel_ids:
        Shape (M,). Integer panel number belonging to every element.
    panel_centers:
        Shape (9, 3).
    panel_boresights:
        Shape (9, 3).
    """
    fractions = np.asarray(side_fractions, dtype=float)
    if fractions.shape != (3, 2):
        raise ValueError("side_fractions must have shape (3, 2).")
    if np.any(fractions <= 0.0) or np.any(fractions >= 1.0):
        raise ValueError("Every side fraction must lie strictly between 0 and 1.")
    if np.any(fractions[:, 0] >= fractions[:, 1]):
        raise ValueError("On each side, the first panel must precede the second.")

    vertices = triangle_vertices(side_length, height)
    vertex_withoutheight = vertices - np.array([0, 0, height])

    vertex_panel_list = []
    vertex_boresight_list = []
    for i in range(len(vertices)):
        vertex_boresight = _unit(vertex_withoutheight[i])
        vertex_boresight_list.append(vertex_boresight)
        vertex_horizontal, vertex_vertical = panel_axes_from_boresight(
            vertex_boresight
        )
        vertice_panel = make_panel(
            vertices[i],
            vertex_horizontal,
            vertex_vertical,
            num_horizontal,
            num_vertical,
            spacing,
        )
        vertex_panel_list.append(vertice_panel)

    vertice_panel = np.vstack(vertex_panel_list)
    vertice_boresight = np.vstack(vertex_boresight_list)

    fraction_boresight_list = []
    fraction_panel_list = []
    fraction_center_list = []

    for v in range(len(vertices)):
        v_start = vertices[v]
        v_end = vertices[(v + 1) % 3]
        side_boresight = _unit(
            (v_start + v_end) / 2 - np.array([0, 0, height])
        )
        fraction_horizontal, fraction_vertical = panel_axes_from_boresight(
            side_boresight
        )

        for a in side_fractions[v]:
            fraction_boresight_list.append(side_boresight)
            side_center = v_start + a * (v_end - v_start)
            fraction_center_list.append(side_center)
            f_panel = make_panel(
                side_center,
                fraction_horizontal,
                fraction_vertical,
                num_horizontal,
                num_vertical,
                spacing,
            )
            fraction_panel_list.append(f_panel)

    fractions_boresight = np.vstack(fraction_boresight_list)
    fractions_panel = np.vstack(fraction_panel_list)
    fractions_center = np.vstack(fraction_center_list)

    element_positions = np.vstack((vertice_panel, fractions_panel))
    panel_centers = np.vstack((vertices, fractions_center))
    panel_boresights = np.vstack((vertice_boresight, fractions_boresight))

    num = num_horizontal * num_vertical
    panel_ids = np.zeros(9 * num, dtype=np.int64)
    for i in range(1, 10, 1):
        for x in range((i - 1) * num, i * num):
            panel_ids[x] = i - 1

    return element_positions, panel_ids, panel_centers, panel_boresights


def make_uniform_triangular_tower(
    side_length: float,
    height: float,
    num_horizontal: int,
    num_vertical: int,
    spacing: float,
) -> tuple[FloatArray, NDArray[np.int64], FloatArray, FloatArray]:
    """Convenience wrapper for uniform fractions 1/3 and 2/3."""
    fractions = np.tile(np.array([1.0 / 3.0, 2.0 / 3.0]), (3, 1))
    return make_triangular_tower(
        side_length,
        height,
        fractions,
        num_horizontal,
        num_vertical,
        spacing,
    )