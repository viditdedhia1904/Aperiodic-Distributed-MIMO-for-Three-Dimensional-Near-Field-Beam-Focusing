"""Numerical measurements for focal regions and unwanted lobes."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike


def power_to_db(power: ArrayLike, reference_power: float | None = None) -> np.ndarray:
    """Convert non-negative power values to dB.

    If no reference is supplied, use the maximum power. Clip very small values
    before log10 so that the result never contains negative infinity.
    """
    # TODO 9: implement 10*log10(power/reference_power).
    raise NotImplementedError("Complete power_to_db() in metrics.py.")


def focal_width_1d(coordinate: ArrayLike, power: ArrayLike, threshold_db: float = -3.0) -> float:
    """Width of the connected above-threshold interval containing the peak.

    Work left and right from the peak index until the power first falls below
    ``threshold_db``. Return the coordinate difference between the two
    threshold-crossing samples.
    """
    # TODO 10: normalize to dB, locate the peak and search left/right.
    raise NotImplementedError("Complete focal_width_1d() in metrics.py.")


def strongest_outside_lobe_db(
    power: ArrayLike,
    points: ArrayLike,
    focus_point: ArrayLike,
    guard_radius: float,
) -> float:
    """Strongest normalized value outside a spherical guard region.

    Return the result in dB relative to the power at the strongest grid point.
    The returned value is normally negative, for example -8.5 dB.
    """
    # TODO 11:
    # 1. Calculate every observation point's distance from the focus.
    # 2. Keep only points outside guard_radius.
    # 3. Find the maximum outside power.
    # 4. Return 10*log10(max_outside/max_all).
    raise NotImplementedError("Complete strongest_outside_lobe_db().")


def volume_margin_db(power: ArrayLike, inside_mask: ArrayLike, outside_mask: ArrayLike) -> float:
    """Minimum-inside to maximum-outside power margin in dB."""
    # TODO 12: return 10*log10(min_inside/max_outside).
    raise NotImplementedError("Complete volume_margin_db() later.")

