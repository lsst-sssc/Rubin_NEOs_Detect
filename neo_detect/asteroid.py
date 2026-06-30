import math

class Asteroid:
    H = None

    def __init__(self, diameter: float , albedo: float = 0.14):
        self.diameter = diameter
        self.albedo = albedo

        # Initialize H
        self.H = self.abs_mag()

    def abs_mag(self):
        """
        Converts diameter to H magnitude (using class variables self.diameter and self.albedo)
        Reference: CNEOS Asteroid Size Estimator (https://cneos.jpl.nasa.gov/tools/ast_size_est.html)

        Returns
        -------
        float
            Absolute magnitude, H
        """
        H = 15.618 - 5 * math.log10(self.diameter / 1000.0) - 2.5 * math.log10(self.albedo)
        return H
