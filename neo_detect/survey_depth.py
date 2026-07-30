import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
import numpy as np

import pandas as pd
from astropy.time import Time

import matplotlib.pyplot as plt

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
        if not isinstance(date, datetime):
            raise TypeError(f"date must be a datetime, got {type(date)}")
        
        # Convert the input date to MJD in UTC, since observationStartMJD is in UTC
        target_mjd = Time(date, scale="utc").mjd
        # If TAI, use Time(date, scale="tai").utc.mjd instead but be wary of mixing timescales
        
        # Restrict to the requested band and guard against an empty selection
        subset = self.observations[self.observations["band"] == band]
        if subset.empty:
            raise ValueError(f"No observations available in band {band}")

        # Find the row with the minimum absolute difference in MJD
        nearest_idx = (subset["observationStartMJD"] - target_mjd).abs().idxmin()
        nearest_row = subset.loc[nearest_idx]

        matched_mjd =float(nearest_row["observationStartMJD"])
        delta_mjd = abs(matched_mjd - target_mjd)

        # Optionally, reject if the nearest visit is too far from the target date
        if delta_mjd > 1.0:  # Example tolerance of 1 day
            raise ValueError(f"No observations within 1 day of {date} in band {band}")
        
        return float(nearest_row["fiveSigmaDepth"])
    
    def _read_observations(self) -> pd.DataFrame:
            query = f"SELECT {', '.join(self.COLUMNS)} FROM observations"
            con = sqlite3.connect(f"file:{self.db_path}?mode=ro", uri=True)
            try:
              return pd.read_sql_query(query, con)
            finally:
                con.close()  

    def plot_depths(self, band: str):
        """Plot the five-sigma limiting depth over time for a given band.

        Parameters
        ----------
        band : str
            The Rubin band to plot (one of u, g, r, i, z, y).
        """
        subset = self.observations[self.observations["band"] == band]
        if subset.empty:
            raise ValueError(f"No observations available in band {band}")

        plt.figure(figsize=(10, 5))
        plt.plot(subset["observationStartMJD"], subset["fiveSigmaDepth"], marker='o', linestyle='-', markersize=2)
        plt.title(f"Five-Sigma Limiting Depth Over Time in Band {band}")
        plt.xlabel("Observation Start MJD")
        plt.ylabel("Five-Sigma Limiting Depth (mag)")
        plt.grid(True)
        plt.show()


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

    # Reference in case of issues: https://community.lsst.org/t/midpointmjdtai-in-diasource-dp0-3/7866/5


    def _date_to_utc_mjd(self, date: datetime) -> float:
        """Convert a datetime to UTC MJD.

        Naive datetimes are assumed to already be UTC.
        """
        if not isinstance(date, datetime):
            raise TypeError(f"date must be a datetime, got {type(date)}")

        if date.tzinfo is None:
            date = date.replace(tzinfo=timezone.utc)
        else:
            date = date.astimezone(timezone.utc)

        return Time(date, scale="utc").utc.mjd

    def sample_depths(
        self,
        start_date: datetime,
        end_date: datetime,
        band: str,
        n_epochs: int,
        tolerance_days: float = 1.0,
    ) -> pd.DataFrame:
        """Sample n_epochs depths between start_date and end_date.

        The method samples evenly spaced target epochs, then matches each one
        to the nearest visit in the requested band.
        """
        if n_epochs < 1:
            raise ValueError("n_epochs must be >= 1")

        start_mjd = self._date_to_utc_mjd(start_date)
        end_mjd = self._date_to_utc_mjd(end_date)

        if end_mjd <= start_mjd:
            raise ValueError("end_date must be after start_date")

        subset = self.observations[
            (self.observations["band"] == band)
            & (self.observations["observationStartMJD"] >= start_mjd)
            & (self.observations["observationStartMJD"] <= end_mjd)
        ]

        if subset.empty:
            raise ValueError(f"No observations available in band {band} in the requested date range")

        target_mjds = np.linspace(start_mjd, end_mjd, n_epochs)

        rows = []
        for target_mjd in target_mjds:
            nearest_idx = (subset["observationStartMJD"] - target_mjd).abs().idxmin()
            row = subset.loc[nearest_idx]

            matched_mjd = float(row["observationStartMJD"])
            delta_days = abs(matched_mjd - float(target_mjd))

            if delta_days > tolerance_days:
                rows.append(
                    {
                        "target_mjd": float(target_mjd),
                        "matched_mjd": np.nan,
                        "band": band,
                        "fiveSigmaDepth": np.nan,
                        "airmass": np.nan,
                        "delta_days": delta_days,
                    }
                )
                continue

            rows.append(
                {
                    "target_mjd": float(target_mjd),
                    "matched_mjd": matched_mjd,
                    "band": row["band"],
                    "fiveSigmaDepth": float(row["fiveSigmaDepth"]),
                    "airmass": float(row["airmass"]),
                    "delta_days": delta_days,
                }
            )

        return pd.DataFrame(rows)

    @staticmethod
    def build_cutdown_observations(full_db_path: str, out_db_path: str, start_date: datetime, end_date: datetime) -> None:
        if start_date.tzinfo is None:
            start_date = start_date.replace(tzinfo=timezone.utc)
        else:
            start_date = start_date.astimezone(timezone.utc)

        if end_date.tzinfo is None:
            end_date = end_date.replace(tzinfo=timezone.utc)
        else:
            end_date = end_date.astimezone(timezone.utc)

        start_mjd = Time(start_date, scale="utc").utc.mjd
        end_mjd = Time(end_date, scale="utc").utc.mjd

        con = sqlite3.connect(f"file:{full_db_path}?mode=ro", uri=True)
        try:
            obs = pd.read_sql_query(
                """
                SELECT *
                FROM observations
                WHERE observationStartMJD BETWEEN ? AND ?
                """,
                con,
                params=(start_mjd, end_mjd),
            )
        finally:
            con.close()

        out = sqlite3.connect(out_db_path)
        try:
            obs.to_sql("observations", out, if_exists="replace", index=False)
        finally:
            out.close()
