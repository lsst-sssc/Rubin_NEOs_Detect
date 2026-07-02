import math
import numpy as np

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

        """
        Computes the phase function for a given phase angle (in degrees) using the Bowell HG system. 
        Reference: Bowell et al. (1989), "Application of photometric models to asteroids". 1989aste.conf..524B

        Returns
        -------
        float
            Phase function value, phi
        """
        phi1 = math.exp(-3.33 * (math.tan(math.radians(angle / 2))) ** 0.63)
        phi2 = math.exp(-1.87 * (math.tan(math.radians(angle / 2))) ** 1.22)

        phase_term = (1 - self.G) * phi1 + self.G * phi2

        return phase_term

    
    def apparent_magnitude(self, r: float, delta: float, phase_angle: float) -> float:

        """
        Computes the apparent magnitude for a given distance and phase angle using the Bowell HG system.
        Reference: Bowell et al. (1989), "Application of photometric models to asteroids". 1989aste.conf..524B

        Returns
        -------
        float
            Apparent magnitude, m
        """
        phi = Asteroid(self.G).phase_function(phase_angle)

        m = self.H + 5 * math.log10(r * delta) - 2.5 * math.log10(phi)

        return m
  
    # r = sqrt(x^2 + y^2) 
    # delta = sqrt((x -x0)^2 + (y - y0)^2)
    # phase_angle = arccos((x*x0 + y*y0) / (r * delta))
    # Basis for Cartesian grid 
    # Calculate for Cartesian grid of x and y coordinates 
    # x = np.linspace(-10, 10, 100) maybe idk??
    # y = np.linspace(-10, 10, 100)
    def cartesian_grid(self, x, y):
        """
        Computes the Cartesian grid for a given set of x and y coordinates, and a reference point (x0, y0).

        Parameters
        ----------
        x - Array of x coordinates.
        y - Array of y coordinates.
        # change later :p

        Returns
        -------
        r - Array of distances from the origin to each point in the grid.
        delta - Array of distances from the reference point (x0, y0) to each point in the grid.
        phase_angle - Array of phase angles for each point in the grid.
        """
        r_2d = np.sqrt(x**2 + y**2)
        delta_2d = np.sqrt((x - 1)**2 + (y)**2)
        phase_angle_2d = np.degrees(np.arccos((r_2d**2 + delta_2d**2 - 1) / (2 * r_2d * delta_2d)))

        return r_2d, delta_2d, phase_angle_2d
    
    def apparent_magnitude_date(self, date: str) -> float:
        """
        Computes the apparent magnitude for a given date using the Bowell HG system.
        Reference: Bowell et al. (1989), "Application of photometric models to asteroids". 1989aste.conf..524B

        Returns
        -------
        float
            Apparent magnitude, m
        """
        # For now, we will use a placeholder for r, delta, and phase_angle based on the date.
        # In a real implementation, these values would be computed based on the asteroid's orbit and the date.
        if date == '2026-07-02':
            r = 1.414  # Placeholder value for distance from Sun in AU
            delta = 1.0  # Placeholder value for distance from Earth in AU
            phase_angle = 45.0  # Placeholder value for phase angle in degrees
        else:
            raise ValueError("Date not supported in this placeholder implementation.")

        m = self.apparent_magnitude(r, delta, phase_angle)

        return m