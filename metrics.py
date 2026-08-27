"""Numerical measurements for focal regions and unwanted lobes."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike


def power_to_db(power: ArrayLike, reference_power: float | None = None) -> np.ndarray:
    """Convert non-negative power values to dB.

    If no reference is supplied, use the maximum power. Clip very small values
    before log10 so that the result never contains negative infinity.
    """
    if reference_power is None:
        reference_power = np.max(power)
    safe_power = np.clip(power, a_min=1e-12, a_max=None)
    safe_ref = max(reference_power, 1e-12)
    
    return 10.0 * np.log10(safe_power / safe_ref)
    # TODO 9: implement 10*log10(power/reference_power).
    raise NotImplementedError("Complete power_to_db() in metrics.py.")


def focal_width_1d(coordinate: ArrayLike, power: ArrayLike, threshold_db: float = -3.0) -> float:
    """Width of the connected above-threshold interval containing the peak.

    Work left and right from the peak index until the power first falls below
    ``threshold_db``. Return the coordinate difference between the two
    threshold-crossing samples.
    """
    # TODO 10: normalize to dB, locate the peak and search left/right.
    power = power_to_db(power)
    max_coordinate = np.argmax(power)
    counter =0
    i = power[max_coordinate]
    while i>=threshold_db:
        if max_coordinate+counter< len(power):
            counter+=1
            i = power[max_coordinate+counter]
        else:
            break
    right = max_coordinate + counter-1
    counter =0
    i = power[max_coordinate]
    while i>=threshold_db:
        if max_coordinate-counter>=0:
            counter+=1
            i = power[max_coordinate-counter]
        else:
            break
    left = max_coordinate - counter+1
    return abs(coordinate[right] - coordinate[left])
    
    
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
    power = np.asarray(power, dtype=float)
    points = np.asarray(points, dtype=float)
    focus_point = np.asarray(focus_point, dtype=float)
    
    distance = np.linalg.norm(points - focus_point, axis=-1)
    outside_mask = distance > guard_radius
    max_outside = np.max(power[outside_mask])
    max_all = np.max(power)
    return 10.0*np.log10(max_outside/max_all)
            
    raise NotImplementedError("Complete strongest_outside_lobe_db().")


def volume_margin_db(power: ArrayLike, inside_mask: ArrayLike, outside_mask: ArrayLike) -> float:
    """Minimum-inside to maximum-outside power margin in dB."""
    # TODO 12: return 10*log10(min_inside/max_outside).
    min_inside=np.min(power[inside_mask])
    max_outside=np.max(power[outside_mask])
    return 10.0*np.log10(min_inside/max_outside)
    raise NotImplementedError("Complete volume_margin_db() later.")

