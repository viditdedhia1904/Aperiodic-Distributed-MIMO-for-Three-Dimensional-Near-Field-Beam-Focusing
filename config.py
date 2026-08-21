"""Common parameters for all simulation scripts.

Keep physical and numerical parameters in this file. Do not copy constants
such as the carrier frequency into many different scripts.
"""

from dataclasses import dataclass


SPEED_OF_LIGHT = 3.0e8  # metre/second


@dataclass(frozen=True)
class SimulationConfig:
    """Default values used in the first experiments."""

    carrier_frequency: float = 8.0e9

    # Start with a small panel. The final paper-sized panel is 27 x 134.
    num_horizontal: int = 9
    num_vertical: int = 21

    # Simplified triangular tower used after the single-panel experiments.
    tower_side_length: float = 6.0
    tower_height: float = 5.0
    side_panels_per_side: int = 2

    # Number of observation points processed together.
    chunk_size: int = 1000

    @property
    def wavelength(self) -> float:
        return SPEED_OF_LIGHT / self.carrier_frequency

    @property
    def element_spacing(self) -> float:
        return self.wavelength / 2.0


CONFIG = SimulationConfig()

