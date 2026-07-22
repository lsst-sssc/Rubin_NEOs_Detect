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
    