import os
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from astropy.time import Time
from rubin_scheduler.data import get_data_dir
from rubin_sim.phot_utils import Bandpass, Sed


def calc_colors(sedname='S.dat', filter_dir=None, sed_dir=None):
   """Calculate the colors for a given asteroids SED

   :param sedname: Name of the SED file, defaults to 'S.dat'
   :type sedname: str, optional
   :param filter_dir: Directory containing the filter files, defaults to None
   :type filter_dir: str, optional
   :param sed_dir: Directory containing the SED file, defaults to None
   :type sed_dir: str, optional
   """
   colors = {}
   colors[sedname] = {}

   # Define and read Rubin filters
   filterlist = ("u", "g", "r", "i", "z", "y")
   #TL: set `filter_dir`  as it's done in lines 293-294 of read_filters() in base_obs.py
   if filter_dir is None:
            filter_dir = os.path.join(get_data_dir(), "throughputs/baseline")


   # Read filter throughputs
   lsst = {}
   # TL: loop over filterlist and read each filter using Bandpass.read_throughput(os.path.join(filter_dir, f"{f}.dat"))
   for f in filterlist:
      bp = Bandpass()
      bp.read_throughput(os.path.join(filter_dir, f"total_{f}.dat"))
      lsst[f] = bp

   # Read in V band filter
   # TL: set `v_dir` the way as sed_dir is set, then use vband.read_throughput(os.path.join(v_dir, v_filter))
   v_dir = os.path.join(get_data_dir(), "movingObjects") 
   # to read it (see read_filters() base_obs.py for details)
   v_filter = "harris_V.dat"
   v_band = Bandpass()
   v_band.read_throughput(os.path.join(v_dir, v_filter)) 


   if sed_dir is None:
      sed_dir = os.path.join(get_data_dir(), "movingObjects")

   mo_sed = Sed()
   mo_sed.read_sed_flambda(os.path.join(sed_dir, sedname))
   # Calculate V magnitude using mo_sed.calc_mag(v_band)
   vmag = mo_sed.calc_mag(v_band)

   # Loop over Rubin filters and calculate colors
   for f in filterlist:
      # Calculate Rubin magnitude using mo_sed.calc_mag(lsst[f])
      mo_mag = mo_sed.calc_mag(lsst[f])
      # Calculate color as V - Rubin magnitude and store in colors[sedname][color_name] where color_name is f"V-{f}"
      colors[sedname][f"V-{f}"] = vmag - mo_mag

   return colors

def filter_plot_colors():
   """Return a dictionary of colors for plotting the Rubin filters

   Returns
   -------
   dict
       Dictionary of colors for plotting the Rubin filters
   """
   filter_colors = {
        "u": "#1600EA",
        "g": "#31DE1F",
        "r": "#B52626",
        "i": "#370201",
        "z": "#BA52FF",
        "y": "#61A2B3",
   }

   return filter_colors

def filter_figure_plot(): 
   """Plot the Rubin filters v V-band with colors for plotting

   Returns
   -------
   None
   """
   filter_colors = filter_plot_colors()
   filterlist = ("u", "g", "r", "i", "z", "y")
   plt.figure(figsize=(10, 6))
   for f in filterlist:
      bp = Bandpass()
      bp.read_throughput(os.path.join(get_data_dir(), "throughputs/baseline", f"total_{f}.dat"))
      plt.plot(bp.wavelen, bp.sb, color=filter_colors[f], label=f)
   v_band = Bandpass()
   v_band.read_throughput(os.path.join(get_data_dir(), "movingObjects", "harris_V.dat"))
   plt.plot(v_band.wavelen, v_band.sb, color="black", label="V-band", linestyle="--")
   plt.xlim(300, 1200)
   plt.ylim(0, 1.05)
   plt.xlabel("Wavelength (nm)")
   plt.ylabel("Throughput")
   plt.title("Rubin Filters and V-Band Filters")
   plt.legend()
   plt.grid()
   plt.show()

def truncate_opsim(start_date: datetime | Time,
                   end_date: datetime | Time,
                   db_path: str) -> tuple[Path | None, pd.DataFrame | None]:
   """Truncate an opsim dataframe to the specified date range
   Takes about 10-15 seconds to run on a typical opsim database.

   Parameters
   ----------
   start_date : datetime
         The start date of the truncation.
   end_date : datetime
         The end date of the truncation.
   db_path : str
         The path to the database containing the opsim data.

   Returns
   -------
   new_db_path : Path
         The path to the new database containing the truncated opsim data.
   trunc_df : pandas.DataFrame
         The truncated opsim dataframe.
   """
   import sqlite3

   # 1. Connect to source SQLite database
   try:
       src_con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
   except (sqlite3.OperationalError, sqlite3.DatabaseError):
      print("Error opening OpSim DB {db_path}")
      return None, None

   # 2. Read existing table into a DataFrame
   df = pd.read_sql_query("SELECT * FROM observations", src_con)
   src_con.close()

   # Perform your data modifications on 'df' here...
   if start_date is not None and end_date is not None:
       if type(start_date) is not Time:
           start_date = Time(start_date, scale="utc")
       if type(end_date) is not Time:
           end_date = Time(end_date, scale="utc")

   trunc_df = df[(df['observationStartMJD'] >= start_date.mjd) & (df['observationStartMJD'] <= end_date.mjd)]
   # 3. Write to new SQLite database
   path = Path(db_path)
   root = path.parent / path.stem
   ext = path.suffix
   new_db_path = Path(str(root) + f"_truncated_{int(start_date.mjd)}_{int(end_date.mjd)}" + ext)
   dest_con = sqlite3.connect(new_db_path)
   trunc_df.to_sql("observations", dest_con, if_exists="replace", index=False)

   # 4. Close the connection
   dest_con.close()

   return new_db_path, trunc_df


class RubinDetection: 
   """Class to handle Rubin detection calculations for asteroids
   """
   SED_FILES = {
      's': 'S.dat',
      'c': 'C.dat',
      'd': 'D.dat',
   }

   filter_colors = filter_plot_colors()

   def transform_Vmag(self, vmag, sed_type='s', filter_name='g', filter_dir=None, sed_dir=None):
      """Convert a V-band magnitude into a Rubin/LSST magnitude for a given SED type and filter."""
      sed_type = sed_type.lower()

      if sed_type in self.SED_FILES:
         sedname = self.SED_FILES[sed_type]
      else:
         sedname = sed_type

      filter_name = filter_name.lower()
      if filter_name not in ("u", "g", "r", "i", "z", "y"):
         raise ValueError(f"Unsupported Rubin filter: {filter_name}")

      # Use the same color model already implemented in calc_colors()
      color_data = calc_colors(sedname=sedname, filter_dir=filter_dir, sed_dir=sed_dir)
      color = color_data[sedname][f"V-{filter_name}"]

      return float(vmag) - color


# Doesn't work just yet, keep at it until it does something correctly 

# get vmag into routine 
# transform vmag class <band>, class will take a band (g or whatever)
# take sed and default to s type as default 
# add other c and d types later 
# copy expected colors dictionary and add it in here 
