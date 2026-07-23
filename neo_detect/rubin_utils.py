import os

from rubin_scheduler.data import get_data_dir
from rubin_sim.phot_utils import Bandpass, Sed

def calc_colors(self, sedname='S.dat', filter_dir=None, sed_dir=None):
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
      lsst[f] = Bandpass.read_throughput(os.path.join(filter_dir, f"{f}.dat"))

   # Read in V band filter
   # TL: set `v_dir` the way as sed_dir is set, then use vband.read_throughput(os.path.join(v_dir, v_filter))
   v_dir = os.path.join(get_data_dir(), "throughputs/baseline") 
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
   self.colors[sedname] = {}

   # Loop over Rubin filters and calculate colors
   for f in filterlist:
      # Calculate Rubin magnitude using mo_sed.calc_mag(lsst[f])
      mo_mag = mo_sed.calc_mag(lsst[f])
      # Calculate color as V - Rubin magnitude and store in colors[sedname][color_name] where color_name is f"V-{f}"
      colors[sedname][f"V-{f}"] = vmag - mo_mag

   return colors