import numpy as np


from datetime import datetime
from dataclasses import dataclass


@dataclass
class Constant_Depth:
    m5_depth: float = 24.52  # Rubin r-filter m5 magnitude

    def depth(self, date: datetime) -> float:
        """
        Returns the constant depth for a given date.

        Parameters
        ----------
        date : datetime
            The date for which to compute the depth.

        Reference: Rubin Observatory 'Calculating LSST limiting magnitudes and SNR' https://smtn-002.lsst.io/

        Returns
        -------
        float
            The constant depth.
        """
        return self.m5_depth
    
@dataclass
class Rubin_Detection:
    
    def transform_Vmag(self, H: float, diameter: float, albedo: float) -> float:
        """
        Transforms the m5 r filter magnitude to V-band magnitude using the asteroid's absolute magnitude (H), diameter, and albedo.
        
        Parameters
        ----------
        H : float
            The absolute magnitude of the asteroid.
        diameter : float
            The diameter of the asteroid.
        albedo : float
            The albedo of the asteroid.

        Reference: Rubin Observatory 'Calculating LSST limiting magnitudes and SNR' https://smtn-002.lsst.io/

        Returns
        -------
        float
            The V-band magnitude of the asteroid.
        """

        # Compute the apparent magnitude in the r filter using the asteroid's absolute magnitude (H), diameter, and albedo
        r_mag = H + 5 * np.log10(diameter / 1329) - 2.5 * np.log10(albedo)

        # Transform the r filter magnitude to V-band magnitude using a color transformation
        V_mag = r_mag + 0.44  # This is an approximate transformation; actual transformation may vary

        return V_mag