"""Run small checks after completing each group of TODOs."""

import numpy as np

from beamforming import focus_weights
from channel import distances, field_on_points, steering_vector
from config import CONFIG
from geometry import make_panel, make_uniform_triangular_tower, triangle_vertices


def run_check(name, function):
    try:
        function()
    except NotImplementedError as error:
        print(f"[INCOMPLETE] {name}: {error}")
        return False
    except Exception as error:  # Helpful during early debugging.
        print(f"[FAILED] {name}: {type(error).__name__}: {error}")
        return False
    print(f"[PASSED] {name}")
    return True


def check_panel():
    positions = make_panel(
        center=[0.0, 0.0, 0.0],
        horizontal_axis=[0.0, 1.0, 0.0],
        vertical_axis=[0.0, 0.0, 1.0],
        num_horizontal=3,
        num_vertical=5,
        spacing=0.1,
    )
    assert positions.shape == (15, 3)
    assert np.allclose(np.mean(positions, axis=0), 0.0)
    assert np.isclose(np.ptp(positions[:, 1]), 0.2)
    assert np.isclose(np.ptp(positions[:, 2]), 0.4)


def check_triangle():
    vertices = triangle_vertices(6.0, 5.0)
    assert vertices.shape == (3, 3)
    pairwise = distances(vertices, vertices)
    nonzero = pairwise[pairwise > 1.0e-12]
    assert np.allclose(nonzero, 6.0)


def check_tower():
    positions, panel_ids, centers, boresights = make_uniform_triangular_tower(
        side_length=6.0,
        height=5.0,
        num_horizontal=3,
        num_vertical=5,
        spacing=0.1,
    )
    assert positions.shape == (135, 3)
    assert panel_ids.shape == (135,)
    assert centers.shape == (9, 3)
    assert boresights.shape == (9, 3)
    assert np.all(np.bincount(panel_ids) == 15)
    assert np.allclose(np.linalg.norm(boresights, axis=1), 1.0)
    for panel_index in range(9):
        panel_mean = positions[panel_ids == panel_index].mean(axis=0)
        assert np.allclose(panel_mean, centers[panel_index])


def check_distances():
    points = np.array([[3.0, 4.0, 0.0], [0.0, 0.0, 5.0]])
    positions = np.array([[0.0, 0.0, 0.0], [3.0, 0.0, 0.0]])
    result = distances(points, positions)
    expected = np.array([[5.0, 4.0], [5.0, np.sqrt(34.0)]])
    assert result.shape == (2, 2)
    assert np.allclose(result, expected)


def check_single_antenna_channel():
    positions = np.array([[0.0, 0.0, 0.0]])
    point = np.array([3.0, 4.0, 0.0])
    a = steering_vector(point, positions, CONFIG.wavelength, include_pathloss=False)
    assert a.shape == (1,)
    assert np.isclose(abs(a[0]), 1.0)


def check_focusing():
    positions = make_panel(
        center=[0.0, 0.0, 0.0],
        horizontal_axis=[0.0, 1.0, 0.0],
        vertical_axis=[0.0, 0.0, 1.0],
        num_horizontal=5,
        num_vertical=7,
        spacing=CONFIG.element_spacing,
    )
    focus = np.array([20.0, 0.0, 0.0])
    weights = focus_weights(focus, positions, CONFIG.wavelength)
    assert np.isclose(np.linalg.norm(weights), 1.0)

    test_points = np.array(
        [
            [20.0, 0.0, 0.0],
            [20.0, 1.0, 0.0],
            [20.0, -1.0, 0.0],
        ]
    )
    field = field_on_points(
        test_points,
        positions,
        weights,
        CONFIG.wavelength,
        chunk_size=2,
    )
    assert np.argmax(np.abs(field) ** 2) == 0


if __name__ == "__main__":
    checks = [
        ("Task 1 - rectangular panel geometry", check_panel),
        ("Task 2 - equilateral triangle geometry", check_triangle),
        ("Task 3 - triangular tower construction", check_tower),
        ("Task 4 - Euclidean distances", check_distances),
        ("Task 5 - steering vector", check_single_antenna_channel),
        ("Tasks 6-7 - field evaluation and point focusing", check_focusing),
    ]
    for check_name, check_function in checks:
        if not run_check(check_name, check_function):
            break
