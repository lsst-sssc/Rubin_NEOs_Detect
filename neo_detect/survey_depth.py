import sqlite3

import pandas as pd

from astropy.time import Time
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


class OpSim_Depth:
    """Per-visit survey depth read from a Rubin/LSST OpSim cadence database.

    Loads the per-visit five-sigma limiting magnitude and the associated
    observing conditions from an OpSim sqlite3 database (as written by
    ``rubin_scheduler``'s ``SchemaConverter.obs2opsim``). Only the columns
    needed for the NEO detectability calculation are read.

    Column reference: https://rubin-scheduler.lsst.io/fbs-output-schema.html

    Notes on the time column: ``observationStartMJD`` is the MJD when the
    shutter opens (the real per-visit time). ``flush_by_mjd`` is a scheduler
    queue-flush deadline, not a visit timestamp, so it is not used here.

    Parameters
    ----------
    db_path : str
        Path to the OpSim sqlite3 database file.

    Attributes
    ----------
    observations : pandas.DataFrame
        One row per visit, with columns given by ``COLUMNS``.
    """

    COLUMNS = ("observationStartMJD", "band", "fiveSigmaDepth", "airmass")

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.observations = self._read_observations()

    def depth(self, date: datetime, band: str) -> float:
        """Return the five-sigma limiting depth for the visit nearest in time.

        Looks up the visit in the requested ``band`` whose observation time is
        closest to ``date`` and returns its ``fiveSigmaDepth``.

        Parameters
        ----------
        date : datetime
            The time of interest.
        band : str
            The Rubin band to match (one of u, g, r, i, z, y).

        Returns
        -------
        float
            The five-sigma limiting magnitude of the nearest matching visit.
        """
        target_mjd = Time(date, scale="utc").mjd
        # if TAI, use Time(date, scale="tai").utc.mjd instead but be wary of mixing timescales
        
        subset = self.observations[self.observations["band"] == band]
        if subset.empty:
            raise ValueError(f"No observations available in band {band}")

        # Find the row with the minimum absolute difference in MJD
        nearest_idx = (subset["observationStartMJD"] - target_mjd).abs().idxmin()
        nearest_row = subset.loc[nearest_idx]

        return nearest_row["fiveSigmaDepth"]

    def _read_observations(self) -> pd.DataFrame:
        query = f"SELECT {', '.join(self.COLUMNS)} FROM observations"
        con = sqlite3.connect(f"file:{self.db_path}?mode=ro", uri=True)
        try:
            return pd.read_sql_query(query, con)
        finally:
            con.close()   




    # Steps to implement:
    # 1. Convert `date` to an MJD on the SAME timescale as the OpSim
    #    column. Per the schema docs, observationStartMJD is UTC (even
    #    though the rest of Rubin uses TAI), so build an astropy Time with
    #    the timescale matching `date` and read Time(...).utc.mjd -- do not
    #    silently mix UTC and TAI (~37 s error). If `date` is naive, decide
    #    and document which timescale it is assumed to be in.
    # 2. Restrict self.observations to rows where band == `band`, and guard
    #    against an empty selection (no coverage in that band).
    # 3. Find the row minimising abs(observationStartMJD - target_mjd),
    #    e.g. (subset["observationStartMJD"] - target_mjd).abs().idxmin().
    # 4. Optionally reject the match if the nearest visit is further from
    #    `date` than some tolerance (i.e. no real observation near `date`).
    # 5. Return that row's fiveSigmaDepth. Consider whether the caller also
    #    needs the matched MJD / airmass (the actual observing conditions),
    #    in which case return a small record instead of a bare float.