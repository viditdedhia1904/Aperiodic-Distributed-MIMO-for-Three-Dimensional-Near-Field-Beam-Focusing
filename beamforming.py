"""Beamforming weights for point and multi-point focusing."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray

from channel import steering_vector


ComplexArray = NDArray[np.complex128]


def focus_weights(
    focus_point: ArrayLike,
    element_positions: ArrayLike,
    wavelength: float,
    include_pathloss: bool = False,
) -> ComplexArray:
    """Create unit-norm weights that focus at one point.

    If ``a`` is the propagation/steering vector at the desired point, use its
    complex conjugate and normalize the result to Euclidean norm one.

    Check: ``np.linalg.norm(weights)`` should be approximately 1.
    """
    # TODO 7: call steering_vector(), conjugate it and normalize it.
    raise NotImplementedError("Complete focus_weights() in beamforming.py.")


def multi_focus_weights(
    anchor_points: ArrayLike,
    coefficients: ArrayLike,
    element_positions: ArrayLike,
    wavelength: float,
) -> ComplexArray:
    """Combine several point-focusing vectors into one beam.

    This is a later task. If there are L anchor points, create L focusing
    vectors, multiply them by the L complex coefficients, add them, and
    normalize the final vector.
    """
    anchor_points = np.asarray(anchor_points, dtype=float)
    coefficients = np.asarray(coefficients, dtype=complex)
    if anchor_points.ndim != 2 or anchor_points.shape[1] != 3:
        raise ValueError("anchor_points must have shape (L, 3).")
    if coefficients.shape != (anchor_points.shape[0],):
        raise ValueError("coefficients must have shape (L,).")

    # TODO 8: implement the multi-anchor combination described above.
    raise NotImplementedError("Complete multi_focus_weights() later.")

