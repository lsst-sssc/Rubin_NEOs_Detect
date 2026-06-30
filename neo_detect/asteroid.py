import math

class Asteroid:
    H = None

    def __init__(self, diameter: float, albedo: float = 0.14, G: float = 0.15):
        self.diameter = diameter
        self.albedo = albedo
        self.G = G

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
        H = 15.618 - 5 * math.log10(self.diameter / 1000) - 2.5 * math.log10(self.albedo)
        print(f"D = {self.diameter}, H = {H}")
        return H
    
    def phase_function(self, angle: float):
        phi1 = math.exp(-3.33 * (math.tan(math.radians(angle / 2))) ** 0.63)
        phi2 = math.exp(-1.87 * (math.tan(math.radians(angle / 2))) ** 1.22)

        phase_term = (1 - self.G) * phi1 + self.G * phi2

        return phase_term

    
    def apparent_magnitude(self, r: float, delta: float, phase_angle: float) -> float:

        phi = Asteroid(self.G).phase_function(phase_angle)

        m = self.H + 5 * math.log10(r * delta) - 2.5 * math.log10(phi)

        return m
  
    
