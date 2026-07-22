import os

from rubin_scheduler.data import get_data_dir
from rubin_sim.phot_utils import Bandpass, Sed

def calc_colors(sedname='S.dat', sed_dir=None):
    if sed_dir is None:
       sed_dir = os.path.join(get_data_dir(), "movingObjects")
    mo_sed = Sed()
    print(sed_dir, mo_sed)