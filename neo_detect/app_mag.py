import math
from neo_detect.phase_fnc import Phase_Function

class Apparent_Magnitude:
    def __init__(self, H: float, G: float = 0.15):
        self.H = H
        self.G = G

    def apparent_magnitude(self, r: float, delta: float, phase_angle: float) -> float:

        phase_angle_rad = math.radians(phase_angle)

        phi = Phase_Function(phase_angle_rad, self.G).phase_function()

        m = self.H + 5 * math.log10(r * delta) - 2.5 * math.log10(phi)

        return m