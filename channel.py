"""Exact spherical-wave propagation functions."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray


FloatArray = NDArray[np.float64]
ComplexArray = NDArray[np.complex128]


def distances(points: ArrayLike, element_positions: ArrayLike) -> FloatArray:
    """Calculate every point-to-element Euclidean distance.

    Parameters
    ----------
    points:
        Array with shape (Q, 3), or one point with shape (3,).
    element_positions:
        Array with shape (M, 3).

    Returns
    -------
    distance_matrix:
        Shape (Q, M).

    Hint
    ----
    Reshape a single point to (1, 3), then use
    ``points[:, None, :] - elements[None, :, :]``.
    """
    # TODO 4: implement using NumPy broadcasting and np.linalg.norm.
    points = np.asarray(points, dtype=float)
    element_positions = np.asarray(element_positions, dtype=float)
    if points.ndim == 1:
        points = points.reshape(1, 3)
    diff = points[:, None, :] - element_positions[None, :, :]
    distance_matrix = np.linalg.norm(diff, axis=-1)
    return distance_matrix
    raise NotImplementedError("Complete distances() in channel.py.")
    


def steering_vector(
    point: ArrayLike,
    element_positions: ArrayLike,
    wavelength: float,
    include_pathloss: bool = False,
) -> ComplexArray:
    point = np.asarray(point,dtype=float)
    element_positions = np.asarray(element_positions,dtype=float)
    k=2*np.pi/wavelength
    d=distances(point,element_positions)[0]
    if include_pathloss:
        steering_array = np.exp(-1j*k*d)/d
    else:
        steering_array = np.exp(-1j*k*d)
    return steering_array
    """Return propagation coefficients from all elements to one point.

    Without path loss:
        a_m(u) = exp(-j k d_m(u))

    With path loss:
        a_m(u) = exp(-j k d_m(u)) / d_m(u)

    The returned array must have shape (M,).
    """
    # TODO 5:
    # 1. Calculate k = 2*pi/wavelength.
    # 2. Obtain the distances for the single point.
    # 3. Form np.exp(-1j * k * d).
    # 4. Divide by d only when include_pathloss is True.
    raise NotImplementedError("Complete steering_vector() in channel.py.")


def field_on_points(
    points: ArrayLike,
    element_positions: ArrayLike,
    weights: ArrayLike,
    wavelength: float,
    include_pathloss: bool = False,
    chunk_size: int = 1000,
) -> ComplexArray:
    """Evaluate the transmitted field at many observation points.

    Process the points in chunks. For every chunk, create a propagation matrix
    A with shape (chunk_points, M), then calculate ``A @ weights``.
    Never create a distance matrix for the complete large grid.
    """
    points = np.asarray(points, dtype=float)
    if points.ndim != 2 or points.shape[1] != 3:
        raise ValueError("points must have shape (Q, 3).")
    positions = np.asarray(element_positions, dtype=float)
    weights = np.asarray(weights, dtype=complex)
    if positions.ndim != 2 or positions.shape[1] != 3:
        raise ValueError("element_positions must have shape (M, 3).")
    if weights.shape != (positions.shape[0],):
        raise ValueError("weights must have shape (M,).")

    field = np.empty(points.shape[0], dtype=complex)
    k = 2.0 * np.pi / wavelength

    for start in range(0, points.shape[0], chunk_size):
        stop = min(start + chunk_size, points.shape[0])
        point_chunk = points[start:stop]
        distance_matrix = distances(point_chunk,element_positions)
        A = np.exp(-1j*k*distance_matrix)
        if include_pathloss:
            A=A/distance_matrix
        field[start:stop] = np.matmul(A,weights)
            
            

        # TODO 6:
        # 1. Calculate a distance matrix for point_chunk.
        # 2. Form A = exp(-1j*k*distance_matrix).
        # 3. If requested, divide A by the distance matrix.
        # 4. Store A @ weights in field[start:stop].

    return field
    raise NotImplementedError("Complete the chunk calculation in field_on_points().")
