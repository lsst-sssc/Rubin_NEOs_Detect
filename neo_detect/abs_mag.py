import math

class Asteroid:
    def __init__(self, diameter: float , albedo: float = 0.14):
        self.diameter = diameter
        self.albedo = albedo

    def abs_mag(self):

        H = 15.618 - 5 * math.log10(self.diameter / 1000.0) - 2.5 * math.log10(self.albedo)
        return H
