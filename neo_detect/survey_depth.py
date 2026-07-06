from datetime import datetime

class Constant_Depth:
    def __init__(self):
        self.depth = 23.70 # Rubin u-filter m5 magnitude 

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
        return self.depth